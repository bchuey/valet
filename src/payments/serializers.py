from payments.models import PaymentMethod

from rest_framework import serializers

class PaymentMethodSerializer(serializers.ModelSerializer):


	class Meta:

		model = PaymentMethod
		fields = ('id', 'customer', 'customer_stripe_id','is_active','is_primary')
		read_only_fields = ('customer','customer_stripe_id')
		depth = 1
		