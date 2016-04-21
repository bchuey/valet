from celeryapp.celery import app
from datetime import datetime, timedelta

from accounts.models import User

from orders.models import ScheduledRepark
from orders.serializers import ScheduledReparkSerializer

import redis

from geopy.distance import vincenty

"""
==============
Celery Tasks
==============
- user creates scheduledrepark
- *views.py*: created scheduledrepark(); .save() to db; run celery tasks.assign_valet_to_scheduled_repark.delay()
	- time is parking_exp_time minus 45 mins



// Second task
- ping locations of all valets
- check to see if is_available
- use matching algorithm to send repark requests to appropriate valet
- ** one repark <=> one valet **
- then next request is up in queue

"""
@app.task(name='query_repark')
def query_repark(repark_id):

	scheduled_repark = ScheduledRepark.objects.get(id=repark_id)

	
	
# use <name>.apply_async(eta=) on views.py
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

		location2 = (valet.valet_start_pos.lat, valet.valet_start_pos.lng)
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

	"""
	Alternatively, a much more complex solution, 
	you would want to use Channels to set up a WebSocket 
	listening to a pubsub system where you send that data.
	"""

	# redis pub/sub
	r = redis.StrictRedis()
	channel = scheduled_repark.request_uuid
	r.publish("valets", data)

	return Response(data)

	

# if you want to assign the closest valet,
# you must grab their position
# and save that position