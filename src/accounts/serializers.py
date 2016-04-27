from accounts.models import User, RegisteredVehicle, DriversLicense, InsurancePolicy

from locations.serializers import LocationSerializer

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

	current_position = LocationSerializer()

	class Meta:

		model = User
		fields = ('id', 'email', 'first_name', 'last_name', 'date_of_birth','password','is_active', 'profile_pic','is_admin','is_valet', 'current_position')
		depth = 2

		
class RegisteredVehicleSerializer(serializers.ModelSerializer):

	class Meta:

		model = RegisteredVehicle
		fields = ('id', 'owned_by', 'make', 'model', 'color','year','license_plate_number', 'updated_registration_tags','parking_permit_zone',)
		read_only_fields = ('vehicle_pic',)
		depth = 2

class DriversLicenseSerializer(serializers.ModelSerializer):

	class Meta:

		model = DriversLicense
		fields = ('id', 'owned_by', 'legal_first_name', 'legal_last_name', 'date_of_birth','license_id_number','registered_city', 'registered_state',)
		depth = 2
		

class InsurancePolicySerializer(serializers.ModelSerializer):

	class Meta:

		model = InsurancePolicy
		fields = ('id', 'owner', 'insured_vehicle', 'company', 'policy_number','agent_first_name','agent_last_name', 'agent_phone_number',)
		depth = 2

