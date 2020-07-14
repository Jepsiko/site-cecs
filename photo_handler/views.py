from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Album, Photo


class IndexView(generic.ListView):
	template_name = 'photo_handler/index.html'

	def get_queryset(self):
		return Album.objects.order_by('-pub_date')[:0]