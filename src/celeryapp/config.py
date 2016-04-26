from __future__ import absolute_import

BROKER_URL = 'redis://127.0.0.1:6379/0' # using server 0
BROKER_TRANSPORT = 'redis'  # broker=> where you store tasks in a queue
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'