from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from authentication.forms import LoginForm

from accounts.models import User
from accounts.forms import UserCreationForm
from accounts.serializers import UserSerializer
from accounts import tasks

from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime

class Register(APIView):

	form = UserCreationForm

	def post(self, request, *args, **kwargs):

		data = request.data

		print '=========='
		print data
		print '=========='

		unicode_dob = data['date_of_birth']
		convert_dob = datetime.strptime(unicode_dob, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
		dob = datetime.strptime(convert_dob, '%Y-%m-%d')
		dob = dob.date()
		date_of_birth = dob

		email = data['email']
		first_name = data['first_name']
		last_name = data['last_name']
		password = data['password']

		# not setting this to False if there is no value
		is_valet = data.get('is_valet',False) # else False

		profile_pic = data['profile_pic'] # grab the image FILE

		user = User.objects.create_user(email, first_name, last_name, date_of_birth, password)

		user.profile_pic = profile_pic
		user.save()

		# import celery task
		# tasks.resize_profile_img.delay((user.id, user.profile_pic.path),countdown=60)

		authenticated_user = authenticate(username=user.email, password=user.password)
		if authenticated_user is not None:

			if authenticated_user.is_active:

				login(request, authenticated_user)

				print authenticated_user.email + 'is logged in!'

				# serialize User
				serializer = UserSerializer(authenticated_user)
				data = serializer.data
				return Response(data)

				# check in Angular controller if the user is_valet 
				# redirect to respective map pages in Angular controller

			else:

				return render(request, self.template, context)				

		return render(request, self.template, context)


class Login(APIView):

	form = LoginForm

	def post(self, request, *args, **kwargs):

		

		# form = self.form(request.POST)
		# context = {
		# 	'form': form,
		# }
		# if request.method == "POST":
		data = request.data

		email = data.get('email', None)
		password = data.get('password', None)
		# if form.is_valid():

		# email = form.cleaned_data.get('email')
		# password = form.cleaned_data.get('password')

	
		user = authenticate(username=email, password=password)

		if user is not None:
			if user.is_active:

				login(request, user)
				print "User logged in"

				serializer = UserSerializer(user)
				data = serializer.data

				return Response(data)

				

def logout_user(request):
		
	logout(request)
	return HttpResponseRedirect('%s'%(reverse('login')))


