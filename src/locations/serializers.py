from locations.models import Location

from rest_framework import serializers

class LocationSerializer(serializers.ModelSerializer):

	class Meta:

		model = Location
		fields = ('id','lat', 'lng', 'full_address')
		depth = 1

