from __future__ import unicode_literals

from django.db import models

from accounts.models import PARKING_ZONES


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


class IntersectionLatLng(models.Model):

	lat = models.FloatField(verbose_name='latitude', max_length=255, null=True, blank=True)
	lng = models.FloatField(verbose_name='longitude', max_length=255, null=True, blank=True)
	parking_section = models.ForeignKey('ParkingSection', related_name='coordinates')

	class Meta:

		db_table = 'intersections'

	def __unicode__(self):

		return unicode(self.id)

	def __str__(self):

		return str(self.id)


class ParkingSection(models.Model):

	label = models.CharField(max_length=2, choices=PARKING_ZONES)
	time_limit = models.IntegerField()
	# accepted_permit = models.ForeignKey(ParkingPermit)


	class Meta:

		db_table = 'parking_sections'

	def __unicode__(self):

		return unicode(self.label)

	def __str__(self):

		return self.label

# class ParkingPermit(models.Model):







