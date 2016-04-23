from django.contrib import admin

from locations.models import IntersectionLatLng, ParkingSection

# Register your models here.

class IntersectionLatLngAdmin(admin.ModelAdmin):



	model = IntersectionLatLng
	list_display = ('id','parking_section', 'lat', 'lng')
	fieldset = (
		('Parking Section', {'fields': ('parking_section',)}),
		('Lat/Lng', {'fields': ('lat','lng')}),
	)

admin.site.register(IntersectionLatLng,IntersectionLatLngAdmin)
admin.site.register(ParkingSection)