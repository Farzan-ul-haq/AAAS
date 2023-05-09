import time

from celery import shared_task

from core.models import ClientActivity, User

@shared_task
def add_client_activity(text, user_id, redirect_url):
    u = User.objects.get(id=user_id)
    ClientActivity.objects.create(
        user=u,
        content=text,
        redirect_url=redirect_url
    )
    return

