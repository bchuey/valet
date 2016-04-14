
from django.conf.urls import include, url
from . import views

app_name = 'accounts'

urlpatterns = [


	url(r'^dashboard/profile/$', views.UserProfileView.as_view(), name='profile'),
	# url(r'^dashboard/requests/$', views.UserRequestsListView.as_view(), name='user-requests'),
	url(r'^dashboard/vehicle/$', views.RegisteredVehicleView.as_view(), name='vehicle'),
	url(r'^dashboard/license/$', views.DriversLicenseView.as_view(), name='license'),
	url(r'^dashboard/insurance-policy/$', views.InsurancePolicyView.as_view(), name='insurance'),


	url(r'^valet/dashboard/profile', views.ValetProfileView.as_view(), name='valet-profile'),
	url(r'^valet/dashboard/history', views.ValetRequestsListView.as_view(), name='valet-history'),
	# url(r'^valet/dashboard/payment', , name='valet-payment'),
	# url(r'^valet/dashboard/license', , name='valet-license'),

]