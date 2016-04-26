from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.models import User
from accounts.serializers import UserSerializer

from locations.models import Location, IntersectionLatLng, ParkingSection
from locations.serializers import IntersectionLatLngSerializer, ParkingSectionSerializer
from locations.forms import LocationForm

from payments.models import PaymentMethod


from orders import tasks
from orders.models import Repark, Dropoff, ScheduledRepark
from orders.serializers import ReparkSerializer, DropoffSerializer, ScheduledReparkSerializer
from orders.forms import OrderForm

from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

import datetime
import redis
import json
import pytz
import stripe

stripe_sk = settings.STRIPE_TEST_SECRET_KEY

timezone.activate(pytz.timezone('America/Los_Angeles'))
local_time_now = timezone.localtime(timezone.now())


# ==================
# Decorators
# ==================
def is_valet_check(user):

	return user.is_valet



# =================
# User FBVs
# =================
@api_view(['POST',])
@login_required(login_url=settings.LOGIN_URL)
def customer_submits_valet_request(request, format=None):

	customer = request.user

	request.session['customer_id'] = customer.id

	if request.method == "POST":

		form = OrderForm(request.POST)

		if form.is_valid():


			print request.POST

			# users current position
			location = Location()
			location.lat = request.POST['lat']
			location.lng = request.POST['lng']
			location.full_address = request.POST['address']
			location.save()

			if request.POST['is_repark']:

				# create Repark instancee
				repark = Repark()
				repark.requested_by = customer
				repark.pickup_location = location
				repark.requested_at = local_time_now
				repark.save()
				request.session["repark_id"] = repark.id

				serializer = ReparkSerializer(repark)

			if request.POST['is_dropoff']:

				# retrieve latest request
				last_request = customer.orders_repark_customer_related.latest('completed_at')
				
				# create Dropoff instance
				dropoff = Dropoff()
				dropoff.requested_by = customer

				# vehicle pickup location is the last request's dropoff location
				dropoff.pickup_location = last_request.dropoff_location
				# vehicle dropoff location is location of user's current position
				dropoff.dropoff_location = location
				dropoff.requested_at = local_time_now
				dropoff.save()
				request.session["dropoff_id"] = dropoff.id

				serializer = DropoffSerializer(dropoff)
			
			if request.POST['is_scheduled_repark']:

				scheduled_repark = ScheduledRepark()
				scheduled_repark.requested_by = customer
				scheduled_repark.pickup_location = location
				scheduled_repark.scheduled_start_date = request.POST['scheduled_start_date']
				scheduled_repark.scheduled_end_date = request.POST['scheduled_end_date']
				scheduled_repark.time_limit = request.POST['time_limit']
				scheduled_repark.requested_at = local_time_now

				"""
				Calculate the expiration time based on when user requested repark
				"""

				parking_exp_time = local_time_now + datetime.timedelta(hours=int(scheduled_repark.time_limit))
				scheduled_repark.parking_exp_time = parking_exp_time


				scheduled_repark.save()

				request.session["scheduled_repark_id"] = scheduled_repark.id

				serializer = ScheduledReparkSerializer(scheduled_repark)


				# send repark to celery task queue
				# eta should be 30 to 45 mins before parking_exp_time

				# tasks.query_valets.apply_async((scheduled_repark.id,), link=tasks.match_valet_with_repark.s(scheduled_repark.id))
				tasks.match_valet_with_repark.apply_async(scheduled_repark.id, countdown=60)

			data = serializer.data
			print(data)

			return Response(data, template_name='maps/user/index.html')


@api_view(['GET',])
@login_required(login_url=settings.LOGIN_URL)
def repark_closed(request):

	if request.method == "GET":

		repark = Repark.objects.get(id=request.session["repark_id"])

		serializer = ReparkSerializer(repark)
		data = serializer.data

		del request.session["repark_id"]

		return Response(data, template_name='maps/user/index.html')




@api_view(['GET',])
@login_required(login_url=settings.LOGIN_URL)
def retrieve_latest_request(request):

	user = request.user

	if request.method == "GET":

		latest_request = Repark.objects.all().filter(requested_by=user).latest('completed_at')

		if latest_request:
			serializer = ReparkSerializer(latest_request)
			data = serializer.data
			print ("retrieving latest request")
			return Response(data, template_name='maps/user/index.html')
		else:

			data = "Oops, you don't have any request."
			return Response(data, template_name='maps/user/index.html')


# =================
# Valet FBVs
# =================
@api_view(['POST',])
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_valet_check)
def valet_accepts_request(request):

	if request.method == "POST":

		valet = request.user

		# valet_starting_position = Location()
		# valet_starting_position.lat = request.POST['lat']
		# valet_starting_position.lng = request.POST['lng']
		# valet_starting_position.save()
		valet_starting_position = valet.current_position

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

		if request.POST['scheduled_repark_id']:

			scheduled_repark = ScheduledRepark.objects.get(id=request.POST['scheduled_repark_id'])
			scheduled_repark.valet_start_pos = valet_starting_position
			scheduled_repark.in_progress = True
			scheduled_repark.save()

			

			request.session["scheduled_repark_id"] = scheduled_repark.id
			
			serializer = ScheduledReparkSerializer(scheduled_repark)

		valet.is_available = False
		valet.save()

		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')


@api_view(['POST',])
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_valet_check)
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

		if 'scheduled_repark_id' in request.session:

			scheduled_repark = ScheduledRepark.objects.get(id=request.session["scheduled_repark_id"])
			scheduled_repark.picked_up_at = local_time_now
			scheduled_repark.save()
			serializer = ScheduledReparkSerializer(scheduled_repark)

		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')
		

@api_view(['POST',])
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_valet_check)
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

		if 'scheduled_repark_id' in request.session:

			scheduled_repark = ScheduledRepark.objects.get(id=request.session["scheduled_repark_id"])
			scheduled_repark.enroute_at = local_time_now
			scheduled_repark.save()

			user = scheduled_repark.requested_by

			serializer = ScheduledReparkSerializer(scheduled_repark)

		data = serializer.data


		if user.registered_vehicle.all()[0].parking_permit_zone:
			# based on User's parking permit
			# query respective ParkingSection

			"""
			- queries specific parking zone
			- grabs boundary coordinates
			- use coordinates to draw boundary on client map
			"""

			parking_permit_zone = user.registered_vehicle.all()[0].parking_permit_zone
			# prkg_section = ParkingSection.objects.all().filter(label='A')
			prkg_section = ParkingSection.objects.all().filter(label=parking_permit_zone)

			coordinates = prkg_section[0].coordinates.all()
			coordinates = IntersectionLatLngSerializer(coordinates,many=True)
			coordinates = coordinates.data

			context = json.dumps({'order':data, 'coordinates':coordinates})

		else:

			context = data

		return Response(context, template_name='maps/valet/index.html')


@api_view(['POST',])
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_valet_check)
def valet_drops_vehicle_at_new_location(request):

	valet = request.user

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

			valet.is_available = True
			serializer = ReparkSerializer(repark)

		# what to do if the request is a Dropoff
		if 'dropoff_id' in request.session:

			dropoff = Dropoff.objects.get(id=request.session["dropoff_id"])
			dropoff.dropoff_location = dropoff_location
			dropoff.dropped_off_at = local_time_now
			dropoff.save()

			valet.is_available = True
			serializer = DropoffSerializer(dropoff)

		if 'scheduled_repark_id' in request.session:

			scheduled_repark = ScheduledRepark.objects.get(id=request.session["scheduled_repark_id"])
			scheduled_repark.dropoff_location = dropoff_location
			scheduled_repark.dropped_off_at = local_time_now
			scheduled_repark.save()

			valet.is_available = True
			serializer = ScheduledReparkSerializer(scheduled_repark)

		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')

@api_view(['GET',])
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_valet_check)
def valet_returning_home(request):

	if request.method == "GET":
		
		if 'repark_id' in request.session:
			repark = Repark.objects.get(id=request.session["repark_id"])
			serializer = ReparkSerializer(repark)

		if 'dropoff_id' in request.session:
			dropoff = Dropoff.objects.get(id=request.session["dropoff_id"])
			serializer = DropoffSerializer(dropoff)

		if 'scheduled_repark_id' in request.session:
			scheduled_repark = ScheduledRepark.objects.get(id=request.session["scheduled_repark_id"])
			serializer = ScheduledReparkSerializer(scheduled_repark)

		data = serializer.data

		return Response(data, template_name='maps/valet/index.html')


@api_view(['POST',])
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_valet_check)
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
			# customer_primary_payment_method = PaymentMethod.objects.all().filter(customer=customer).filter(is_primary=1)

			# print customer_primary_payment_method[0]

			# customer_id = customer_primary_payment_method[0].customer_stripe_id
			charge_customer(customer)

			del request.session["repark_id"]
			try:
				print(request.session["repark_id"])
			except:
				print("request.session['repark_id'] is deleted")

		if 'dropoff_id' in request.session:

			dropoff = Dropoff.objects.get(id=request.session['dropoff_id'])
			dropoff.is_active = False
			dropoff.in_progress = False
			dropoff.is_completed = True
			dropoff.completed_at = local_time_now
			dropoff.save()

			customer = dropoff.requested_by
			# customer_primary_payment_method = PaymentMethod.objects.all().filter(customer=customer).filter(is_primary=1)
			# customer_id = customer_primary_payment_method[0].customer_stripe_id
			charge_customer(customer)

			del request.session["dropoff_id"]
			try:
				print(request.session["dropoff_id"])
			except:
				print("request.session['dropoff_id'] is deleted")

		if 'scheduled_repark_id' in request.session:

			scheduled_repark = ScheduledRepark.objects.get(id=request.session['scheduled_repark_id'])
			scheduled_repark.is_active = False
			scheduled_repark.in_progress = False
			scheduled_repark.is_completed = True
			scheduled_repark.completed_at = local_time_now
			scheduled_repark.save()

			customer = scheduled_repark.requested_by
			charge_customer(customer)

			del request.session["scheduled_repark_id"]
			try:
				print(request.session["scheduled_repark_id"])
			except:
				print("request.session['scheduled_repark_id'] is deleted")


		return HttpResponseRedirect('%s'%(reverse('valet-map')))


# ==============
# Stripe payments
# ==============
def charge_customer(customer):

	"""
	After the  'request' is complete,
	query customer's payment methods,
	filter cards w/ is_primary tag,
	grab the first one,
	charge the customer 
	"""

	payment_method = customer.payment_method.all().filter(is_primary=1)[0]
	customer_stripe_id = payment_method.customer_stripe_id

	stripe.Charge.create(
	  amount=1500, # $15.00 this time
	  currency="usd",
	  customer=customer_stripe_id # Previously stored, then retrieved
	)

@api_view(['POST',])
def update_current_position(request):

	# print request.POST 	# <QueryDict: {u'lat': [u'37.7082051'], u'lng': [u'-122.4433762']}>
	# print request.POST['lat']
	# print request.POST['lng']
	user = request.user

	current_position = Location()
	current_position.lat = request.POST['lat']
	current_position.lng = request.POST['lng']
	current_position.save()

	print "current position of valet: "
	print current_position.lat
	print current_position.lng
	print "================="

	user.current_position = current_position
	user.save()

	msg = "Updated current position"

	if user.is_valet:
		return Response(msg, template_name='maps/valet/index.html')

	else:
		return Response(msg, template_name='maps/user/index.html')





