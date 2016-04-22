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


# query available valets
# redis publish event
# redis listen for event
	# socket.emit("current-valet-location")
# run ajax POST request
	# save new position
# in callback
	# run match_valet_with_repark

@app.task(name='query_valets')
def query_valets(repark_id):

	valets = User.objects.all().filter(is_valet=1).filter(is_available=1)
	valets = UserSerializer(valets,many=True)
	valets = valets.data


	scheduled_repark = ScheduledRepark.objects.get(id=repark_id)

	serializer = ScheduledReparkSerializer(scheduled_repark)
	data = serializer.data
	# redis pub/sub
	r = redis.StrictRedis()
	channel = scheduled_repark.request_uuid
	r.publish("query_valets", data)



	return valets

@app.task(name='match_valet_with_repark')
def match_valet_with_repark(valets, repark_id):

	scheduled_repark = ScheduledRepark.objects.get(id=repark_id)

	# valets = User.objects.all().filter(is_valet=1).filter(is_available=1)

	"""
	Calculate closest distance in miles
	Assign the closest valet to repark vehicle
	"""
	# print valets
	"""

	{u'profile_pic': u'/media/accounts/thor_thor/profile_pic/thor_tTr6FWt.jpeg', u'first_name': u'thor', u'last_name': u'thor', u'is_active': True, u'id': 17, u'date_of_birth': u'1980-06-06', u'current_position': {u'lat': u'37.708216', u'lng': u'-122.4433882', u'id': 357, u'full_address': None}, u'is_admin': False, u'is_valet': True, u'password': u'pbkdf2_sha256$24000$RE07EBfY6kDk$4XS48kUdEFRK/wJCnwp8aTMTdz7RLfeD4/dlIahHEEo=', u'email': u'thor@gmail.com'}
	"""

	location1 = (scheduled_repark.pickup_location.lat,scheduled_repark.pickup_location.lng)

	# valet = valets[0]
	# print valet
	# print valet['current_position']['lat'], valet['current_position']['lng']

	"""
	[2016-04-22 18:10:33,146: WARNING/Worker-4] {u'profile_pic': u'/media/accounts/thor_thor/profile_pic/thor_tTr6FWt.jpeg', u'first_name': u'thor', u'last_name': u'thor', u'is_active': True, u'id': 17, u'date_of_birth': u'1980-06-06', u'current_position': {u'lat': u'37.708216', u'lng': u'-122.4433882', u'id': 401, u'full_address': None}, u'is_admin': False, u'is_valet': True, u'password': u'pbkdf2_sha256$24000$RE07EBfY6kDk$4XS48kUdEFRK/wJCnwp8aTMTdz7RLfeD4/dlIahHEEo=', u'email': u'thor@gmail.com'}
		[2016-04-22 18:10:33,147: WARNING/Worker-4] 37.708216
		[2016-04-22 18:10:33,147: WARNING/Worker-4] -122.4433882
	"""
	min_distance = 0
	for valet in valets:
		
		if valet['current_position']:
			location2 = (valet['current_position']['lat'], valet['current_position']['lng'])

			distance = vincenty(location1,location2).miles

			if min_distance != 0:
				
				if distance < min_distance:

					min_distance = distance
					assigned_valet = valet

			else:

				min_distance = distance
				assigned_valet = valet
				
				
		else:
			pass

	# print assigned_valet
	assigned_valet = User.objects.get(id=valet['id'])
	print 'the assigned valet is: '
	print assigned_valet

	scheduled_repark.reparked_by = assigned_valet

	scheduled_repark.save()

	serializer = ScheduledReparkSerializer(scheduled_repark)
	data = serializer.data


	json = JSONRenderer().render(data)
	data = json

	# redis pub/sub
	r = redis.StrictRedis()
	channel = scheduled_repark.request_uuid
	r.publish("valets", data)

	print "updated scheduled repark: "
	print data


	return data

