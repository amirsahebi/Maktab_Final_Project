from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrfMaktab.settings')
app = Celery('trainee_service')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logger = get_task_logger(__name__)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from blog.tasks import test_task

    # Executes every 1 minute
    sender.add_periodic_task(
        crontab(minute="*/1"),
        test_task.s(),
    )

    # crontab(hour=1, minute=0, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
