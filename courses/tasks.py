from celery import shared_task
from .services import send_course_update_notifications as send_notifications
from .services import block_inactive_users as block_users


@shared_task
def hello():
    """ Test task """
    print("Hello")


@shared_task
def send_course_update_notifications(course_id):
    """ Celery task for sending notifications. """
    send_notifications(course_id)


@shared_task
def block_inactive_users():
    """ Celery task to block inactive users. """
    count = block_users()
    print(f'{count} users blocked.')
