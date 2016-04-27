from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from authentication.forms import LoginForm

from accounts.models import User
from accounts.forms import UserCreationForm
from accounts.serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

class Register(APIView):

	form = UserCreationForm
	template = 'authentication/register.html'

	def get(self, request, *args, **kwargs):

		form = self.form
		context = {
			'form': form,
		}

		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):

		form = self.form(request.POST, request.FILES)

		context = {
			'form': form,
		}

		print "-----------"
		print "new user register:"
		print request.POST
		print "------------"

		if form.is_valid():

			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			date_of_birth = form.cleaned_data.get('date_of_birth')
			password = form.cleaned_data.get('password1')


			user = User.objects.create_user(email,date_of_birth,first_name,last_name,password)
			user.is_valet = request.POST.get('is_valet', False)
			user.profile_pic = request.FILES['profile_pic']
			user.save()
			print "User registered"

			authenticated_user = authenticate(username=email, password=password)
			print "User authenticated"

			if authenticated_user is not None:
				if authenticated_user.is_active:

					login(request, authenticated_user)
					print "User logged in"

					if user.is_valet:
						return HttpResponseRedirect('%s'%(reverse('valet-map')))
					else:
						return HttpResponseRedirect('%s'%(reverse('user-map')))	

					# return HttpResponseRedirect('%s'%(reverse('home')))

				else:

					return render(request, self.template, context)
			else:

				return render(request, self.template, context)				

		return render(request, self.template, context)


class AngularLogin(APIView):

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


