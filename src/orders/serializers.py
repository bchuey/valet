from accounts.models import User
from orders.models import Repark, Dropoff
from locations.serializers import LocationSerializer

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



