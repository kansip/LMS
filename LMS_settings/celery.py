from argparse import Namespace
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS_settings.settings')

app = Celery('tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()