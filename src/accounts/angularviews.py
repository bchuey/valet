
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User, RegisteredVehicle, DriversLicense, InsurancePolicy
from accounts.forms import UserCreationForm, UserChangeForm, RegisteredVehicleForm, DriversLicenseForm, InsurancePolicyForm
from accounts.serializers import UserSerializer, RegisteredVehicleSerializer, DriversLicenseSerializer, InsurancePolicySerializer

from authentication.forms import LoginForm

from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime

# from ..orders.models import Repark

STATIC_LOGIN_URL = '/login/'

# ==================
# Profile
# ==================

class UserProfileView(LoginRequiredMixin, APIView):

	form = UserChangeForm

	def get(self, request, *args, **kwargs):

		user = request.user

		serializer = UserSerializer(user)

		data = serializer.data

		return Response(data)


	def post(self, request, *args, **kwargs):

		data = request.data

		unicode_dob = data['date_of_birth']
		convert_dob = datetime.strptime(unicode_dob, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
		dob = datetime.strptime(convert_dob, '%Y-%m-%d')
		dob = dob.date()

		user = request.user
		user.email = data['email']
		user.first_name = data['first_name']
		user.last_name = data['last_name']
		user.date_of_birth = dob

		user.save()

		serializer = UserSerializer(user)

		data = serializer.data

		return Response(data)

class ValetProfileView(LoginRequiredMixin, View):

	login_url = STATIC_LOGIN_URL
	model = User
	template = 'accounts/valet/dashboard/profile.html'
	form = UserChangeForm

	def get(self, request, *args, **kwargs):

		user = self.request.user
		form = self.form(instance=user)

		context = {
			'user': user,
			'form': form,
		}

		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):

		form = self.form(request.POST)
		if form.is_valid():

			# update
			return HttpResponseRedirect('%s'%(reverse('accounts:valet-profile')))

# ==================
# Add RegisteredVehicle
# ==================
class RegisteredVehicleView(LoginRequiredMixin, APIView):

	form = RegisteredVehicleForm

	def get(self, request, *args, **kwargs):
		
		user = request.user
		
		
		try:

			vehicle = RegisteredVehicle.objects.get(owned_by=user)

			serializer = RegisteredVehicleSerializer(vehicle)

			data = serializer.data

		except:

			data = {"msg": "You did not register your vehicle."}


		return Response(data)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST)
		if form.is_valid():
			user = self.request.user
			try:
				vehicle = RegisteredVehicle.objects.get(owned_by=user)
			except:
				vehicle = RegisteredVehicle()

			vehicle.owned_by = user
			vehicle.make = form.cleaned_data.get('make')
			vehicle.model = form.cleaned_data.get('model')
			vehicle.color = form.cleaned_data.get('color')
			vehicle.license_plate_number = form.cleaned_data.get('license_plate_number')
			vehicle.year = form.cleaned_data.get('year')
			vehicle.updated_registration_tags = form.cleaned_data.get('updated_registration_tags')
			vehicle.parking_permit_zone = form.cleaned_data.get('parking_permit_zone')
			vehicle.save()

			return HttpResponseRedirect('%s'%(reverse('accounts:vehicle')))

# ==================
# Add DriversLicense
# ==================
class DriversLicenseView(LoginRequiredMixin, APIView):
	
	form = DriversLicenseForm

	def get(self, request, *args, **kwargs):
		
		user = request.user


		try:
			drivers_license = DriversLicense.objects.get(owned_by=user)

			serializer = DriversLicenseSerializer(drivers_license)

			data = serializer.data


		except:

			data = {"msg": "No drivers license found."}


		return Response(data)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST)
		if form.is_valid():
			user = self.request.user
			try:
				drivers_license = DriversLicense.objects.get(owned_by=user)
			except:
				drivers_license = DriversLicense()

			drivers_license.owned_by = user
			drivers_license.legal_first_name = form.cleaned_data.get('legal_first_name')
			drivers_license.legal_last_name = form.cleaned_data.get('legal_last_name')
			drivers_license.date_of_birth = form.cleaned_data.get('date_of_birth')
			drivers_license.license_id_number = form.cleaned_data.get('license_id_number')
			drivers_license.registered_city = form.cleaned_data.get('registered_city')
			drivers_license.registered_state = form.cleaned_data.get('registered_state')
			drivers_license.save()
			print("success!")
			return HttpResponseRedirect('%s'%(reverse('accounts:license')))
		# print("form not valid")
		# return HttpResponseRedirect('%s'%(reverse('accounts:profile')))

# ==================
# Add InsurancePolicy
# ==================
class InsurancePolicyView(LoginRequiredMixin, APIView):

	form = InsurancePolicyForm

	def get(self, request, *args, **kwargs):

		user = request.user

		try:
			
			insurance_policy = InsurancePolicy.objects.get(owner=user)

			serializer = InsurancePolicySerializer(insurance_policy)

			data = serializer.data

		except:

			data = {"msg": "No insurance policy on file."}



		return Response(data)

	def post(self, request, *args, **kwargs):

		
		form = self.form(request.POST)
		if form.is_valid():

			user = self.request.user

			try:
				insurance_policy = InsurancePolicy.objects.get(owner=user)
			except:
				insurance_policy = InsurancePolicy()

			insurance_policy.owner = user
			insurance_policy.company = form.cleaned_data.get('company')
			insurance_policy.policy_number = form.cleaned_data.get('policy_number')
			insurance_policy.agent_first_name = form.cleaned_data.get('agent_first_name')
			insurance_policy.agent_last_name = form.cleaned_data.get('agent_last_name')
			insurance_policy.agent_phone_number = form.cleaned_data.get('agent_phone_number')


			# insurance_policy.insured_vehicle = 
			insurance_policy.save()

			return HttpResponseRedirect('%s'%(reverse('accounts:insurance')))

# ==================
# Requests ListView
# ==================

class UserRequestsListView(LoginRequiredMixin, View):

	login_url = STATIC_LOGIN_URL
	model = User
	template = 'accounts/user/dashboard/requests.html'

	def get(self, request, *args, **kwargs):

		user = self.request.user
		# reparks = user.customer_reparks.all().order_by('-requested_at','-completed_at')
		reparks = Repark.objects.all().filter(requested_by=user).order_by('-requested_at', '-completed_at')

		context = {
			'user': user,
			'reparks': reparks,
		}

		return render(request, self.template, context)

# =================
# Valet History
# =================

class ValetRequestsListView(LoginRequiredMixin, View):

	login_url = STATIC_LOGIN_URL
	model = User
	template = 'accounts/valet/dashboard/valet-requests.html'

	def get(self, request, *args, **kwargs):

		user = self.request.user
		# reparks = user.valet_reparks.all().order_by('-completed_at')
		reparks = Repark.objects.all().filter(reparked_by=user).order_by('-completed_at')
		
		context = {
			'reparks': reparks,
		}

		return render(request, self.template, context)