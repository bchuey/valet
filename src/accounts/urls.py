
from django.conf.urls import include, url

from payments.views import PaymentMethodView, update_payment_method

from . import views
from accounts.angularviews import UserProfileView, RegisteredVehicleView, DriversLicenseView, InsurancePolicyView

app_name = 'accounts'

urlpatterns = [


	# url(r'^dashboard/profile/$', views.UserProfileView.as_view(), name='profile'),
	url(r'^dashboard/profile/$', UserProfileView.as_view(), name='profile'),

	# url(r'^dashboard/vehicle/$', views.RegisteredVehicleView.as_view(), name='vehicle'),
	url(r'^dashboard/vehicle/$', RegisteredVehicleView.as_view(), name='vehicle'),

	# url(r'^dashboard/license/$', views.DriversLicenseView.as_view(), name='license'),
	url(r'^dashboard/license/$', DriversLicenseView.as_view(), name='license'),

	# url(r'^dashboard/insurance-policy/$', views.InsurancePolicyView.as_view(), name='insurance'),
	url(r'^dashboard/insurance-policy/$', InsurancePolicyView.as_view(), name='insurance'),




	url(r'^dashboard/payment-method/$', PaymentMethodView.as_view(), name='payment'),
	url(r'^dashboard/payment-method/update/$', update_payment_method, name='update-payment'),


	url(r'^valet/dashboard/profile', views.ValetProfileView.as_view(), name='valet-profile'),
	url(r'^valet/dashboard/history', views.ValetRequestsListView.as_view(), name='valet-history'),
	# url(r'^valet/dashboard/payment', , name='valet-payment'),
	# url(r'^valet/dashboard/license', , name='valet-license'),

]