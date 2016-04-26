from celeryapp.celery import app
from datetime import datetime, timedelta

from accounts.models import User
from accounts.serializers import UserSerializer

from orders.models import ScheduledRepark
from orders.serializers import ScheduledReparkSerializer

import redis
import json

from rest_framework.renderers import JSONRenderer

from geopy.distance import vincenty

