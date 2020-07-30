from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .models import Album, Account, Post, Event
from .forms import RegistrationForm, AccountAuthentificationForm


class IndexView(generic.TemplateView):
	template_name = 'main/index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['latest_album'] = Album.objects.order_by('pub_date').last()
		context['incoming_event'] = Event.objects.order_by('pub_date').last()
		return context


class ComiteView(generic.ListView):
	template_name = 'main/comite.html'
	context_object_name = 'comite'

	def get_queryset(self):
		accounts = Account.objects.exclude(post__isnull=True)
		comite = []
		already_done = []
		for i in range(len(accounts)):
			minimum = None
			for j in range(len(accounts)):
				if j not in already_done and (minimum is None or accounts[j].order() < accounts[minimum].order()):
					minimum = j
			already_done.append(minimum)
			comite.append(accounts[minimum])
		return comite


class PhotoView(generic.ListView):
	template_name = 'main/photo.html'
	context_object_name = 'albums'

	def get_queryset(self):
		return Album.objects.all().order_by('-pub_date')


class AccountView(generic.DetailView):
	model = Account
	template_name = 'main/account.html'

	def get_queryset(self):
		return Account.objects.all()


class PostView(generic.DetailView):
	model = Post
	template_name = 'main/post.html'

	def get_queryset(self):
		return Post.objects.all()


class EventView(generic.DetailView):
	model = Event
	template_name = 'main/event.html'

	def get_queryset(self):
		return Event.objects.all()


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(username=username, password=raw_password)
			login(request, account)
			return redirect('main:index')
		else:
			context['registration_form'] = form
	else:  # GET request
		form = RegistrationForm()
		context['registration_form'] = form

	return render(request, 'main/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('main:index')


def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect('main:index')

	if request.POST:
		form = AccountAuthentificationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return redirect('main:index')
	else:
		form = AccountAuthentificationForm()

	context['login_form'] = form
	return render(request, 'main/login.html', context)