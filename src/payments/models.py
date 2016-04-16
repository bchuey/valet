from __future__ import unicode_literals

from django.db import models


from accounts.models import User

# Create your models here.

class PaymentMethod(models.Model):

	customer = models.ForeignKey(User, related_name='payment_method')
	customer_stripe_id = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_primary = models.BooleanField(default=False)

	class Meta:

		db_table = 'stripe_accounts'

	def __unicode__(self):

		return unicode(self.customer_stripe_id)

	def __str__(self):

		return self.customer_stripe_id