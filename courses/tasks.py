from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from courses.models import Course, Subscription


@shared_task
def hello():
    """ Test task """
    print("Hello")

@shared_task
def send_course_update_notifications(course_id):
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course, is_active=True)

    for subscription in subscriptions:
        user = subscription.user
        subject = f'Course {subscription.course.name} updated'
        message = f'The course {subscription.course.name} you are subscribed to has updated'
        send_mail(subject, message, EMAIL_HOST_USER, [user.email])
        print(f'message sent to {user.email}')
