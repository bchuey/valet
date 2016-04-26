from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','valet.settings')

django.setup()

# instantiate celery object

app = Celery('valet')

app.config_from_object('django.conf:settings') # use project settings as settings file

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 	# look for tasks.py file in all apps 
