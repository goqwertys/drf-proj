from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
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
    """ User model """
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    date = models.DateTimeField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(
        max_length=3,
        choices=METHOD_CHOISES,
        default='CRD',
        verbose_name='payment method'
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
        super().save(*args, **kwargs)

    def get_service(self):
        return self.course or self.lesson

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
