from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone

from .models import Album, Account, Post, Event, Chant, Journal, PV
from .forms import RegistrationForm, AccountAuthentificationForm, AccountUpdateForm


class IndexView(generic.TemplateView):
	template_name = 'main/index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['latest_album'] = Album.objects.order_by('pub_date').last()
		context['incoming_event'] = Event.objects.filter(pub_date__gte=timezone.now()).order_by('pub_date').first()
		context['ongoing_event'] = Event.objects.filter(pub_date__lte=timezone.now(), end_date__gte=timezone.now()).order_by('pub_date').first()
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


class JournalView(generic.ListView):
	template_name = 'main/journal.html'
	context_object_name = 'journals'

	def get_queryset(self):
		return Journal.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class ArchivesView(generic.ListView):
	template_name = 'main/archives.html'
	context_object_name = 'pvs'

	def get_queryset(self):
		return PV.objects.all().order_by('-pub_date')


class ChantView(generic.ListView):
	template_name = 'main/chants.html'
	context_object_name = 'chants'

	def get_queryset(self):
		return Chant.objects.all().order_by('order')


class EventsView(generic.ListView):
	template_name = 'main/events.html'
	context_object_name = 'events'

	def get_queryset(self):
		return Event.objects.all().order_by('-pub_date')


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


class AlbumView(generic.DetailView):
	model = Album
	template_name = 'main/album.html'

	def get_queryset(self):
		return Album.objects.all()


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


def profile_view(request):
	if not request.user.is_authenticated:
		return redirect('main:login')

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
	else:
		account = Account.objects.filter(username=request.user.username)[0]
		form = AccountUpdateForm(initial={
			'photo': account.photo,
			'description': account.description,
			'display_email': account.display_email,
			'phone_number': account.phone_number,
			'display_phone_number': account.display_phone_number,
		})

	context['profile_form'] = form
	return render(request, 'main/profile.html', context)
