from django import forms

from orders.models import Repark, Dropoff, ScheduledRepark

import datetime

# today = datetime.date.today().strftime('%Y-%m-%d')
today = datetime.date.today()


class OrderForm(forms.Form):

	class  Meta:

		fields = (
			'address',
			'lat',
			'lng',
			'is_repark',
			'is_dropoff',
			'scheduled_start_date',
			'scheduled_end_date',
			'time_limit',
			'is_scheduled_repark'
		)


	def clean_address(self):
		pass

	def clean_lat(self):
		
		LAT_REGEX = re.compile(r'^[0-9]+\.{1}[0-9]+$')
		lat = self.cleaned_data.get('lat')
		if not LAT_REGEX.match(lat):
			raise forms.ValidationError('Invalid latitude coordinate')

		return lat

	def clean_lng(self):

		LNG_REGEX = re.compile(r'^\-[0-9]+\.{1}[0-9]+$')
		lng = self.cleaned_data.get('lng')
		if not LNG_REGEX.match(lng):
			raise forms.ValidationError('Invalid longitude coordinate')

		return lng

	def clean_is_repark(self):
		pass

	def clean_is_dropoff(self):
		pass

	def clean_is_scheduled_repark(self):
		pass

	def clean_scheduled_start_date(self):
		
		start_date = self.cleaned_data.get('scheduled_start_date')
		if start_date < today:
			raise forms.ValidationError('Start date can not be a past date.')

		return start_date

	def clean_scheduled_end_date(self):
		
		start_date = self.cleaned_data.get('scheduled_start_date')
		end_date = self.cleaned_data.get('scheduled_end_date')
		if end_date < today or end_date < start_date:
			raise forms.ValidationError('End date has to be date after start date.')

		return end_date

	def clean_time_limit(self):
		
		TIME_LIMIT_REGEX = re.compile(r'^[0-9]{1}$')
		time_limit = self.cleaned_get('time_limit')
		if not TIME_LIMIT_REGEX.match(time_limit):
			raise forms.ValidationError('Re-enter the # of hours you can park here.')

		return time_limit