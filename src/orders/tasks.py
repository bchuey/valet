from celeryapp.celery import app
from datetime import datetime, timedelta

from accounts.models import User

from orders.models import ScheduledRepark
from orders.serializers import ScheduledReparkSerializer

import redis

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
def query_valets():

	valets = User.objects.all().filter(is_valet=1).filter(is_available=1)

	# redis pub/sub
	r = redis.StrictRedis()
	channel = scheduled_repark.request_uuid
	r.publish("query_valets", data)

	return Response(data)

@app.task(name='match_valet_with_repark')
def match_valet_with_repark(repark_id):

	scheduled_repark = ScheduledRepark.objects.get(id=repark_id)

	valets = User.objects.all().filter(is_valet=1).filter(is_available=1)

	"""
	Calculate closest distance in miles
	Assign the closest valet to repark vehicle
	"""

	location1 = (scheduled_repark.pickup_location.lat,scheduled_repark.pickup_location.lng)
	for valet in valets:

		# how do you get the location of the Valet???
		location2 = (valet.current_position.lat, valet.current_position.lng)
		distance = vincenty(location1,location2).miles
		if min_distance:

			if distance < min_distance:

				min_distance = distance
				assigned_valet = valet
		else:

			min_distance = distance

	scheduled_repark.reparked_by = assigned_valet

	scheduled_repark.save()

	serializer = ScheduledReparkSerializer(scheduled_repark)
	data = serializer.data


	# redis pub/sub
	r = redis.StrictRedis()
	channel = scheduled_repark.request_uuid
	r.publish("valets", data)

	return Response(data)

