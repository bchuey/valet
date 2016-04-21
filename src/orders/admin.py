from django.contrib import admin

from orders.models import Repark, Dropoff, ScheduledRepark

# Register your models here.
class ReparkAdmin(admin.ModelAdmin):

	model = Repark
	list_display = (
		'id',
		'requested_by', 
		'reparked_by', 
		'pickup_location', 
		'dropoff_location',
		'requested_at',
		'picked_up_at',
		'dropped_off_at',
		'is_active',
		'in_progress',
		'is_completed',
		'completed_at',
		'request_uuid',
	)

	fieldsets = (
		('IDs',{'fields':('request_uuid',)}),
		('Users',{'fields':('requested_by','reparked_by')}),
		('Locations',{'fields':('pickup_location','dropoff_location','valet_start_pos')}),
		('Status',{'fields':('is_active','in_progress','is_completed')}),
		('Timestamps',{'fields':('requested_at','picked_up_at','enroute_at','dropped_off_at','completed_at')}),
	)

class DropoffAdmin(admin.ModelAdmin):

	model = Dropoff
	list_display = (
		'id',
		'requested_by', 
		'reparked_by', 
		'pickup_location', 
		'dropoff_location',
		'requested_at',
		'picked_up_at',
		'dropped_off_at',
		'is_active',
		'in_progress',
		'is_completed',
		'completed_at',
		'request_uuid',
	)

	fieldsets = (
		('IDs',{'fields':('request_uuid',)}),
		('Users',{'fields':('requested_by','reparked_by')}),
		('Locations',{'fields':('pickup_location','dropoff_location','valet_start_pos')}),
		('Status',{'fields':('is_active','in_progress','is_completed')}),
		('Timestamps',{'fields':('requested_at','picked_up_at','enroute_at','dropped_off_at','completed_at')}),
	)

admin.site.register(ScheduledRepark)
admin.site.register(Repark, ReparkAdmin)
admin.site.register(Dropoff, DropoffAdmin)