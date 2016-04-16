
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from accounts.models import User

from payments.models import PaymentMethod
from payments.forms import AddPaymentMethodForm

import stripe


stripe_sk = settings.STRIPE_TEST_SECRET_KEY

class PaymentMethodView(View):

	form = AddPaymentMethodForm
	template = 'accounts/user/dashboard/subscription.html'

	def get(self, request, *args, **kwargs):

		user = request.user
		payment_methods = user.payment_method.all()
		print payment_methods
		stripe_publishable_key = settings.STRIPE_TEST_PUBLISHABLE_KEY
		form = self.form

		context = {
			'payment_methods': payment_methods,
			'stripe_publishable_key': stripe_publishable_key,
			'form': form,
		}

		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):

		user = request.user
		# Set your secret key: remember to change this to your live secret key in production
		# See your keys here https://dashboard.stripe.com/account/apikeys
		stripe.api_key = stripe_sk

		# Get the credit card details submitted by the form
		token = request.POST['stripeToken']

		# Create a Customer
		customer = stripe.Customer.create(
		  source=token,
		  description='Stripe account for: %s'%(user.email),
		)

		# YOUR CODE: Save the customer ID and other info in a database for later!
		customer_payment_method = PaymentMethod()
		customer_payment_method.customer = user
		customer_payment_method.customer_stripe_id = customer.id
		customer_payment_method.save()

		print customer_payment_method

		return HttpResponseRedirect('%s'%(reverse('accounts:payment')))






		