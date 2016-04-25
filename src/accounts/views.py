
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User, RegisteredVehicle, DriversLicense, InsurancePolicy
from accounts.forms import UserCreationForm, UserChangeForm, RegisteredVehicleForm, DriversLicenseForm, InsurancePolicyForm

from authentication.forms import LoginForm



# from ..orders.models import Repark

STATIC_LOGIN_URL = '/login/'

# ==================
# Profile
# ==================

class UserProfileView(LoginRequiredMixin, View):

	login_url = STATIC_LOGIN_URL
	model = User
	template = 'accounts/user/dashboard/profile.html'
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

			form.save()
			
			return HttpResponseRedirect('%s'%(reverse('accounts:profile')))

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
class RegisteredVehicleView(LoginRequiredMixin, View):

	login_url = STATIC_LOGIN_URL
	model = RegisteredVehicle
	template = 'accounts/user/dashboard/vehicle.html'
	form = RegisteredVehicleForm

	def get(self, request, *args, **kwargs):
		
		user = self.request.user
		
		try:
			vehicle = RegisteredVehicle.objects.get(owned_by=user)
			form = self.form(instance=vehicle)
			print("executed try statement")
		except:
			form = self.form


		context = {
			'form': form,
		}

		return render(request, self.template, context)

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
class DriversLicenseView(LoginRequiredMixin, View):
	
	login_url = STATIC_LOGIN_URL
	model = DriversLicense
	template = 'accounts/user/dashboard/license.html'
	form = DriversLicenseForm

	def get(self, request, *args, **kwargs):
		
		user = self.request.user

		try:
			drivers_license = DriversLicense.objects.get(owned_by=user)
			form = self.form(instance=drivers_license)
		except:
			form = self.form

		context = {
			'user': user,
			'form': form,
		}

		return render(request, self.template, context)

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
class InsurancePolicyView(LoginRequiredMixin, View):

	login_url = STATIC_LOGIN_URL
	model = InsurancePolicy
	template = 'accounts/user/dashboard/insurance_policy.html'
	form = InsurancePolicyForm

	def get(self, request, *args, **kwargs):

		user = self.request.user
		try:
			insurance_policy = InsurancePolicy.objects.get(owner=user)
			form = self.form(instance=insurance_policy)
		except:
			form = self.form

		context = {
			'user': user,
			'form': form,
		}

		return render(request, self.template, context)

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