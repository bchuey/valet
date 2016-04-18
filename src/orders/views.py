from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.conf import settings

from accounts.models import User

from locations.models import Location, IntersectionLatLng, ParkingSection
from locations.serializers import IntersectionLatLngSerializer, ParkingSectionSerializer

from payments.models import PaymentMethod




from orders.models import Repark, Dropoff, ScheduledRepark
from orders.serializers import ReparkSerializer, DropoffSerializer, ScheduledReparkSerializer

from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response

import datetime
import redis
import json
import pytz
import stripe

stripe_sk = settings.STRIPE_TEST_SECRET_KEY

timezone.activate(pytz.timezone('America/Los_Angeles'))
local_time_now = timezone.localtime(timezone.now())

# =================
# User FBVs
# =================
@api_view(['POST',])
def customer_submits_valet_request(request, format=None):

	customer = request.user

	request.session['customer_id'] = customer.id

	if request.method == "POST":

		print request.POST

		# users current position
		location = Location()
		location.lat = request.POST['lat']
		location.lng = request.POST['lng']
		try:
			location.full_address = request.POST['full_address']
		except:
			pass
		location.save()

		if request.POST['is_repark']:

			# create Repark instance
			repark = Repark()
			repark.requested_by = customer
			repark.requested_at = local_time_now
			repark.pickup_location = location
			repark.save()
			request.session["repark_id"] = repark.id

			serializer = ReparkSerializer(repark)

		if request.POST['is_dropoff']:

			# retrieve latest request
			last_request = customer.orders_repark_customer_related.latest('completed_at')
			
			# create Dropoff instance
			dropoff = Dropoff()
			dropoff.requested_by = customer
			dropoff.requested_at = local_time_now

			# vehicle pickup location is the last request's dropoff location
			dropoff.pickup_location = last_request.dropoff_location
			# vehicle dropoff location is location of user's current position
			dropoff.dropoff_location = location
			dropoff.save()
			request.session["dropoff_id"] = dropoff.id

			serializer = DropoffSerializer(dropoff)
		
		if request.POST['is_scheduled_repark']:

			scheduled_repark = ScheduledRepark()
			scheduled_repark.requested_by = customer
			scheduled_repark.requested_at = local_time_now
			scheduled_repark.pickup_location = location
			scheduled_repark.scheduled_start_date = request.POST['scheduled_start_date']
			scheduled_repark.scheduled_end_date = request.POST['scheduled_end_date']
			scheduled_repark.time_limit = request.POST['time_limit']

			"""
			Calculate the expiration time based on when user requested repark
			"""

			# parking_exp_time = local_time_now + request.POST['time_limit']
			# scheduled_repark.parking_exp_time = parking_exp_time
			
			scheduled_repark.save()

			request.session["scheduled_repark_id"] = scheduled_repark.id

			serializer = ScheduledRepark(scheduled_repark)
		
		data = serializer.data
		print(data)

		return Response(data, template_name='maps/user/index.html')


@api_view(['GET',])
def repark_closed(request):

	if request.method == "GET":

		repark = Repark.objects.get(id=request.session["repark_id"])

		serializer = ReparkSerializer(repark)
		data = serializer.data

		del request.session["repark_id"]

		return Response(data, template_name='maps/user/index.html')




@api_view(['GET',])
def retrieve_latest_request(request):

	user = request.user

	if request.method == "GET":

		latest_request = Repark.objects.all().filter(requested_by=user).latest('completed_at')

		if latest_request:
			serializer = ReparkSerializer(latest_request)
			data = serializer.data

			return Response(data, template_name='maps/user/index.html')
		else:

			data = "Oops, you don't have any request."
			return Response(data, template_name='maps/user/index.html')


# =================
# Valet FBVs
# =================
@api_view(['POST',])
def valet_accepts_request(request):

	if request.method == "POST":

		valet = request.user

		valet_starting_position = Location()
		valet_starting_position.lat = request.POST['lat']
		valet_starting_position.lng = request.POST['lng']
		valet_starting_position.save()

		# have to take into account if the request is a Dropoff
		if request.POST['repark_id']:

			repark = Repark.objects.get(id=request.POST['repark_id'])
			repark.reparked_by = valet
			repark.in_progress = True
			repark.valet_start_pos = valet_starting_position
			repark.save()
			# set a 'repark_id' session for the valet
			request.session["repark_id"] = repark.id
			serializer = ReparkSerializer(repark)

		if request.POST['dropoff_id']:

			dropoff = Dropoff.objects.get(id=request.POST['dropoff_id'])
			customer = dropoff.requested_by			
			# grab the last repark request's dropoff location
			latest_repark_request = customer.orders_repark_customer_related.latest('completed_at')
			dropoff.reparked_by = valet
			dropoff.in_progress = True
			dropoff.valet_start_pos = valet_starting_position
			# valet picks up car at user's last repark request's dropoff_location
			dropoff.pickup_location = latest_repark_request.dropoff_location
			dropoff.save()
			request.session["dropoff_id"] = dropoff.id
			serializer = DropoffSerializer(dropoff)

		# if request.POST['scheduled_repark_id']:

		# 	scheduled_repark = ScheduledRepark.objects.get(id=request.POST['scheduled_repark_id'])
		# 	scheduled_repark.reparked_by = valet
		# 	scheduled_repark.save()

			# add this object to a queue here???


		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')


@api_view(['POST',])
def valet_arrives_at_vehicle(request):

	valet = request.user

	# should I just use session/cache ???
	if request.method == "POST":

		if 'repark_id' in request.session:
			
			repark = Repark.objects.get(id=request.session["repark_id"])
			repark.picked_up_at = local_time_now
			repark.save()
			serializer = ReparkSerializer(repark)

		if 'dropoff_id' in request.session:

			dropoff = Dropoff.objects.get(id=request.session["dropoff_id"])
			dropoff.picked_up_at = local_time_now
			dropoff.save()
			serializer = DropoffSerializer(dropoff)

		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')
		

@api_view(['POST',])
def valet_on_route(request):

	valet = request.user

	if request.method == "POST":

		if 'repark_id' in request.session:

			repark = Repark.objects.get(id=request.session["repark_id"])
			repark.enroute_at = local_time_now
			repark.save()

			user = repark.requested_by

			serializer = ReparkSerializer(repark)

		if 'dropoff_id' in request.session:

			dropoff = Dropoff.objects.get(id=request.session["dropoff_id"])
			dropoff.enroute_at = local_time_now
			dropoff.save()

			user = dropoff.requested_by

			serializer = DropoffSerializer(dropoff)


		if user.parking_permit_zone:
			# based on User's parking permit
			# query respective ParkingSection

			"""
			- queries specific parking zone
			- grabs boundary coordinates
			- use coordinates to draw boundary on client map
			"""
			# prkg_section = ParkingSection.objects.all().filter(label='A')
			prkg_section = ParkingSection.objects.all().filter(label=user.parking_permit_zone)

			coordinates = prkg_section[0].coordinates.all()
			coordinates = IntersectionLatLngSerializer(coordinates,many=True)
			coordinates = coordinates.data

		data = serializer.data

		context = json.dumps({'order':data, 'coordinates':coordinates})

		return Response(context, template_name='maps/valet/index.html')


@api_view(['POST',])
def valet_drops_vehicle_at_new_location(request):

	if request.method == "POST":

		dropoff_location = Location()
		dropoff_location.lat = request.POST['lat']
		dropoff_location.lng = request.POST['lng']
		dropoff_location.full_address = request.POST['address']
		dropoff_location.save()

		if 'repark_id' in request.session:
			
			repark = Repark.objects.get(id=request.session["repark_id"])
			repark.dropoff_location = dropoff_location
			repark.dropped_off_at = local_time_now
			repark.save()

			serializer = ReparkSerializer(repark)

		# what to do if the request is a Dropoff
		if 'dropoff_id' in request.session:

			dropoff = Dropoff.objects.get(id=request.session["dropoff_id"])
			dropoff.dropoff_location = dropoff_location
			dropoff.dropped_off_at = local_time_now
			dropoff.save()

			serializer = DropoffSerializer(dropoff)

		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')

@api_view(['GET',])
def valet_returning_home(request):

	if request.method == "GET":
		
		if 'repark_id' in request.session:
			repark = Repark.objects.get(id=request.session["repark_id"])
			serializer = ReparkSerializer(repark)

		if 'dropoff_id' in request.session:
			dropoff = Dropoff.objects.get(id=request.session["dropoff_id"])
			serializer = DropoffSerializer(dropoff)

		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')


@api_view(['POST',])
def request_completed(request):

	stripe.api_key = stripe_sk
	
	if request.method == "POST":

		if 'repark_id' in request.session:

			repark = Repark.objects.get(id=request.session["repark_id"])
			repark.is_active = False
			repark.in_progress = False
			repark.is_completed = True
			repark.completed_at = local_time_now
			repark.save()

			customer = repark.requested_by
			customer_primary_payment_method = PaymentMethod.objects.all().filter(customer=customer).filter(is_primary=1)

			# print customer_primary_payment_method[0]

			customer_id = customer_primary_payment_method[0].customer_stripe_id
			charge_customer(customer_id)

			del request.session["repark_id"]
			try:
				print(request.session["repark_id"])
			except:
				print("repark.session['repark_id'] is deleted")

		if 'dropoff_id' in request.session:

			dropoff = Dropoff.objects.get(id=request.session['dropoff_id'])
			dropoff.is_active = False
			dropoff.in_progress = False
			dropoff.is_completed = True
			dropoff.completed_at = local_time_now
			dropoff.save()

			customer = dropoff.requested_by
			customer_primary_payment_method = PaymentMethod.objects.all().filter(customer=customer).filter(is_primary=1)
			customer_id = customer_primary_payment_method.customer_stripe_id
			charge_customer(customer_id)

			del request.session["dropoff_id"]
			try:
				print(request.session["dropoff_id"])
			except:
				print("repark.session['dropoff_id'] is deleted")

		return HttpResponseRedirect('%s'%(reverse('valet-map')))


def charge_customer(customer_id):

	stripe.Charge.create(
	  amount=1500, # $15.00 this time
	  currency="usd",
	  customer=customer_id # Previously stored, then retrieved
	)




