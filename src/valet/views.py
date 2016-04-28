from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class Home(TemplateView):

	template_name = 'base.html' 	# /templates/base.html


class UserMap(TemplateView):

	template_name = 'maps/user/index.html'


class ValetMap(TemplateView):

	template_name = 'maps/valet/index.html'


