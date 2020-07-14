from django.urls import path
from . import views

app_name = 'photo_handler'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
]