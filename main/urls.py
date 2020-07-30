from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('comite/', views.ComiteView.as_view(), name='comite'),
	path('comite/<int:pk>', views.AccountView.as_view(), name='account'),
	path('post/<int:pk>', views.PostView.as_view(), name='post'),
	path('event/<int:pk>', views.EventView.as_view(), name='event'),
	path('register/', views.registration_view, name='register'),
	path('logout/', views.logout_view, name='logout'),
	path('login/', views.login_view, name='login'),
	path('profile/', views.profile_view, name='profile'),
	path('photo/', views.PhotoView.as_view(), name='photo'),
]
