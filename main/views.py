from django.shortcuts import render
from django.views import generic

from .models import Album, Photo


class IndexView(generic.ListView):
	template_name = 'main/index.html'

	def get_queryset(self):
		return Album.objects.order_by('-pub_date')[:0]
