"""valet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from authentication.views import Register, Login, logout_user
from authentication.angularviews import AngularLogin

from orders.views import (
    customer_submits_valet_request, 
    valet_accepts_request, 
    valet_arrives_at_vehicle,
    valet_on_route,
    valet_drops_vehicle_at_new_location,
    valet_returning_home,
    request_completed,
    retrieve_latest_request,
    update_current_position,
)


from . import views

urlpatterns = [

    # authentication
	url(r'^register/$', Register.as_view(), name='register'),
    # url(r'^login/$', Login.as_view(), name='login'),
    url(r'^login/$', AngularLogin.as_view(), name='login'),
    url(r'^logout/$', logout_user, name='logout'),

    # respective homepages
    url(r'^user/$', views.UserMap.as_view(), name='user-map'),
    url(r'^valet/$', views.ValetMap.as_view(), name='valet-map'),

    # requests
    url(r'^user/request/valet/$', customer_submits_valet_request, name='request-valet'),
    url(r'^user/request/latest/$', retrieve_latest_request, name='latest-request'),
    url(r'^user/send-current-location/$', update_current_position, name='user-update-position'),
    url(r'^valet/request/accept/$', valet_accepts_request, name='accept-request'),
    url(r'^valet/request/arrived/$', valet_arrives_at_vehicle, name='arrived'),
    url(r'^valet/request/enroute/$', valet_on_route, name='enroute'),
    url(r'^valet/request/reparked/$', valet_drops_vehicle_at_new_location, name='reparked'),
    url(r'^valet/request/return/$', valet_returning_home, name='return'),
    url(r'^valet/request/completed/$', request_completed, name='completed'),
    url(r'^valet/send-current-location/$', update_current_position, name='update-position'),

    # base index/home page
	url(r'^$', views.Home.as_view(), name='home'),
    url(r'^accounts/', include('accounts.urls')),

    # admin
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
