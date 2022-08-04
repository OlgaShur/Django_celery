import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_HW.settings')

app = Celery('Django_HW')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'newsapp.tasks.notify_category_update',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': ('agrs'),
    }
}
