from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):
	
	lat = models.CharField(verbose_name='latitude', max_length=255, null=True, blank=True)
	lng = models.CharField(verbose_name='longitude', max_length=255, null=True, blank=True)
	full_address = models.CharField(verbose_name='full address', max_length=255, null=True, blank=True)

	class Meta:

		db_table = 'gps_locations'

	def __unicode__(self):

		return unicode(self.id) or u''

	def __str__(self):

		return str(self.id)