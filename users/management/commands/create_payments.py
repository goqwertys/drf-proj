from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils import timezone
from courses.models import Course, Lesson
from users.models import User, Payment

class Command(BaseCommand):
    help = 'Create sample payments, users, courses, and lessons'

    def handle(self, *args, **kwargs):
        # Создание пользователя
        user, created = User.objects.get_or_create(
            email='example@example.com',
            defaults={
                'password': make_password('1234'),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created user'))
        else:
            self.stdout.write(self.style.WARNING('User already exists'))

        # Создание курса
        course, created = Course.objects.get_or_create(
            name='Python Course',
            defaults={
                'description': 'Learn Python programming',
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created course'))
        else:
            self.stdout.write(self.style.WARNING('Course already exists'))

        # Создание урока
        lesson, created = Lesson.objects.get_or_create(
            title='Introduction to Python',
            defaults={
                'course': course,
                'preview': 'path/to/lesson_preview.jpg',
                'video_url': 'https://example.com/video'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created lesson'))
        else:
            self.stdout.write(self.style.WARNING('Lesson already exists'))

        # Создание платежей
        Payment.objects.create(
            user=user,
            date=timezone.now(),
            course=course,
            lesson=None,
            amount=100.0,
            method='CRD'
        )

        Payment.objects.create(
            user=user,
            date=timezone.now(),
            course=None,
            lesson=lesson,
            amount=50.0,
            method='CSH'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created payments'))
