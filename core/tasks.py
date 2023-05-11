from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email(email, subject, content):
    """
    CELERY TASK TO SEND EMAIL
    """
    print('sending email')
    send_mail(
        subject,
        content,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print('email sent')
    return