from __future__ import unicode_literals

from django.db import models


from accounts.models import User
from locations.models import Location

import uuid
# Create your models here.
class Order(models.Model):

	request_uuid = models.UUIDField(default=uuid.uuid4)
	requested_by = models.ForeignKey(User, verbose_name='customer', related_name='%(app_label)s_%(class)s_customer_related', null=True, blank=True)
	reparked_by = models.ForeignKey(User, verbose_name='valet', related_name='%(app_label)s_%(class)s_valet_related', null=True, blank=True)
	pickup_location = models.ForeignKey(Location, verbose_name='pickup location', related_name='%(app_label)s_%(class)s_pickup_loc_related', null=True, blank=True)
	dropoff_location = models.ForeignKey(Location, verbose_name='dropoff location', related_name='%(app_label)s_%(class)s_dropoff_loc_related', null=True, blank=True)
	requested_at = models.DateTimeField()
	picked_up_at = models.DateTimeField(null=True, blank=True)
	enroute_at = models.DateTimeField(null=True, blank=True)
	dropped_off_at = models.DateTimeField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	in_progress = models.BooleanField(default=False)
	is_completed = models.BooleanField(default=False)
	completed_at = models.DateTimeField(null=True,blank=True)
	valet_start_pos = models.ForeignKey(Location, related_name='%(app_label)s_%(class)s_related', null=True, blank=True)

	class Meta:

		abstract = True


class ScheduledRepark(Order):
	
	scheduled_start_date = models.DateField() 	# default today
	scheduled_end_date = models.DateField()
	time_limit = models.IntegerField()
	parking_exp_time = models.DateTimeField()
	is_scheduled_repark = models.BooleanField(default=True)

	class Meta:

		db_table = 'scheduled_reparks'

	def __unicode__(self):

		return unicode(self.id)

	def __str__(self):

		return str(self.id)

class Repark(Order):

	is_repark = models.BooleanField(default=True)

	class Meta(Order.Meta):

		db_table = 'reparks'

	def __unicode__(self):

		return unicode(self.id)

	def __str__(self):

		return str(self.id)

class Dropoff(Order):

	is_dropoff = models.BooleanField(default=True)

	class Meta(Order.Meta):

		db_table = 'dropoffs'

	def __unicode__(self):

		return unicode(self.id)

	def __str__(self):

		return str(self.id)
