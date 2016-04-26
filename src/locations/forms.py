from django import forms

from locations.models import Location

class LocationForm(forms.ModelForm):

	class Meta:

		model = Location
		fields = ('lat','lng','full_address')

	def clean_lat(self):
		pass

	def clean_lng(self):
		pass

	def clean_full_address(self):
		pass