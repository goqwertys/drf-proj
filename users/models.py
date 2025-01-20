from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import URLField, CharField
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    """ Custom user model manager where email is the unique identifiers for authentication """
    def create_user(self, email, password=None, **extra_fields):
        """ Create and save a User with the given email and password """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ Create and save a SuperUser with the given email and password """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone_number = PhoneNumberField(
        verbose_name='phone number',
        help_text='enter your phone number',
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=100,
        verbose_name='city',
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to='users/avatars',
        verbose_name='avatar',
        help_text='upload your avatar',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email


class Payment(models.Model):
    METHOD_CHOISES = [
        ('CRD', 'By card'),
        ('CSH', 'By cash')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        help_text='Please specify user'
    )
    date = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    method = models.CharField(
        max_length=3,
        choices=METHOD_CHOISES,
        default='CRD',
        verbose_name='payment method'
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Session ID',
        help_text='Please specify session id'
    )
    link = URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Payment link',
        help_text='Please specify payment link'
    )
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Payment status'
    )

    def __str__(self):
        return f'{str(self.user)} - {str(self.date)} - {str(self.amount)}'

    def clean(self):
        if self.course and self.lesson:
            raise ValidationError('Payment cannot be associated with both a course and a lesson.')

        if not self.course and not self.lesson:
            raise ValidationError('Payment must be associated with either a course or a lesson.')

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.amount:
            if self.course:
                self.amount = self.course.amount
            elif self.lesson:
                self.amount = self.lesson.amount

        super().save(*args, **kwargs)

    def get_service(self):
        return self.course or self.lesson

    def update_status(self, status):
        if status in dict(self.STATUS_CHOICES):
            self.status = status
            self.save()
        else:
            raise ValueError(f'Invalid status {status}')

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
