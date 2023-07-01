from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

from core.models import Product, ProductClick, ProductImpression

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

@shared_task
def create_impresion_obj(products):
    for product_id in products:
        ProductImpression.objects.create(
            product=Product.objects.get(id=product_id)
        )

@shared_task
def create_click_obj(products):
    for product_id in products:
        ProductClick.objects.create(
            product=Product.objects.get(id=product_id)
        )
