import os

from celery import Celery

from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ellipsis_django_task.settings')

app = Celery('ellipsis_django_task')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# For linux you can embed beat in worker process i.e celery -A rikolto_workspace worker -B -l INFO
# celery -A ellipsis_django_task beat -l INFO
# celery -A ellipsis_django_task worker -l INFO

# RabitMQ Commands
# systemctl enable rabbitmq-server
# systemctl status rabbitmq-server

 

app.conf.beat_schedule = {
    # Executes every morning at 09:00 a.m.
    'scheduled_loan_reminder_message': {
        'task': 'administrator.tasks.send_reminder_message',
        'schedule': crontab(hour=9, minute=0),
    },
    # Executes every morning at 08:00 a.m.
    'scheduled_loan_deadline_message': {
        'task': 'administrator.tasks.send_deadline_message',
        "schedule": crontab(hour=8, minute=0),
        # "schedule": 10,
    },
}
