from accounts.models import User
from orders.models import Repark, Dropoff, ScheduledRepark
from locations.serializers import LocationSerializer
from accounts.serializers import UserSerializer

from rest_framework import serializers

class ReparkSerializer(serializers.ModelSerializer):

	pickup_location = LocationSerializer()
	dropoff_location = LocationSerializer()
	valet_start_pos = LocationSerializer()

	class Meta:

		model = Repark
		fields = ('id','request_uuid', 'is_repark', 'requested_by','reparked_by','pickup_location','dropoff_location','requested_at','picked_up_at','dropped_off_at', 'is_active', 'in_progress','is_completed','valet_start_pos')
		depth = 2

class DropoffSerializer(serializers.ModelSerializer):

	pickup_location = LocationSerializer()
	dropoff_location = LocationSerializer()
	valet_start_pos = LocationSerializer()
	
	class Meta:

		model = Dropoff
		fields = ('id','request_uuid', 'is_dropoff', 'requested_by','reparked_by','pickup_location','dropoff_location','requested_at','picked_up_at','dropped_off_at', 'is_active', 'in_progress','is_completed','valet_start_pos')
		depth = 2


class ScheduledReparkSerializer(serializers.ModelSerializer):


	requested_by = UserSerializer()
	reparked_by = UserSerializer()
	pickup_location = LocationSerializer()
	dropoff_location = LocationSerializer()
	valet_start_pos = LocationSerializer()

	class  Meta:

		model = ScheduledRepark
		fields = ('id','request_uuid', 'is_scheduled_repark', 'requested_by','reparked_by','pickup_location','dropoff_location','requested_at','picked_up_at','dropped_off_at', 'is_active', 'in_progress','is_completed','valet_start_pos', 'scheduled_start_date','scheduled_end_date','time_limit','parking_exp_time')
		depth = 2