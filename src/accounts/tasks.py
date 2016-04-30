from celeryapp.celery import app
from datetime import datetime, timedelta

from accounts.models import User
from accounts.serializers import UserSerializer

import redis
import json

from rest_framework.renderers import JSONRenderer
from PIL import Image


@app.task(name='resize_profile_img')
def resize_profile_img(request, user_id, img_filename):

	user = User.objects.get(id=user_id)

	size = 100, 100

	img = Image.open(img_filename)
	img.thumbnail(size)
	img.save(file, "JPEG")

	user.profile_pic_small = img
	user.save()

	"""
	When user registers, before saving the image into database,
	grab the image and create to different sizes.

	"""

	return user

