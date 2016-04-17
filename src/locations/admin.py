from django.contrib import admin

from locations.models import IntersectionLatLng, ParkingSection

# Register your models here.

admin.site.register(IntersectionLatLng)
admin.site.register(ParkingSection)