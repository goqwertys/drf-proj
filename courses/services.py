from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER, BLOCK_PERIOD_DAYS
from courses.models import Course, Subscription
from users.models import User


def send_course_update_notifications(course_id):
    """ Sends notifications about course updates. """
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course, is_active=True)

    for subscription in subscriptions:
        user = subscription.user
        subject = f'Course {course.name} updated'
        message = f'The course {course.name} you are subscribed to has updated'
        send_mail(subject, message, EMAIL_HOST_USER, [user.email])
        print(f'Message sent to {user.email}')


def block_inactive_users():
    """ Blocks users whose last login was after a certain period. """
    period = timezone.now() - timedelta(days=BLOCK_PERIOD_DAYS)
    active_users = User.objects.filter(last_login__gt=period)
    count = active_users.update(is_active=False)
    print(f'Blocked {count} active users.')
    return count
