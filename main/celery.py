import os, time

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

app = Celery("main")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

from celery import shared_task
@shared_task
def add(x, y):
    print('STARTING', str(x), str(y))
    time.sleep(10)
    print('DONE', str(x), str(y))
    return x + y