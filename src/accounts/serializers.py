from accounts.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

	class Meta:

		model = User
		fields = ('id', 'email', 'first_name', 'last_name', 'date_of_birth','password','is_active','is_admin','is_valet')
		
