from locations.models import Location, ParkingSection, IntersectionLatLng

from rest_framework import serializers

class LocationSerializer(serializers.ModelSerializer):

	class Meta:

		model = Location
		fields = ('id','lat', 'lng', 'full_address')
		depth = 1


class IntersectionLatLngSerializer(serializers.ModelSerializer):

	class Meta:

		model = IntersectionLatLng
		fields = ('id','lat','lng','parking_section')
		depth = 1

class ParkingSectionSerializer(serializers.ModelSerializer):

	coordinates = IntersectionLatLngSerializer(many=True, read_only=True)

	class Meta:

		model = ParkingSection
		fields = ('id', 'label', 'time_limit', 'coordinates')
		depth = 2

