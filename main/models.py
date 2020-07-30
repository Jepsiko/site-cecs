from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator


class Album(models.Model):
	name = models.CharField(max_length=30)
	pub_date = models.DateField()

	def __str__(self):
		return self.name

	def get_photos(self):
		return Photo.objects.filter(album=self)


class Photo(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='gallery')

	def __str__(self):
		return self.image.name


class Event(models.Model):
	name = models.CharField(max_length=30)
	affiche = models.ImageField(upload_to='affiches')
	facebook_link = models.URLField(max_length=200)
	pub_date = models.DateField(blank=True)
	description = models.TextField(blank=True)


class MyAccountManager(BaseUserManager):
	def create_user(self, username, email, first_name, last_name, password=None):
		if not username:
			raise ValueError('Users must have a username')
		if not email:
			raise ValueError('Users must have an email address')
		if not first_name:
			raise ValueError('Users must have a first name')
		if not last_name:
			raise ValueError('Users must have a last name')

		user = self.model(
			username=username,
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
		)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, username, email, first_name, last_name, password):
		user = self.create_user(
			username=username,
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
			password=password,
		)

		user.is_admin = True
		user.is_member = True
		user.is_staff = True
		user.is_superuser = True

		user.save(using=self._db)
		return user


class Post(models.Model):
	name = models.CharField(max_length=30, unique=True)
	order = models.IntegerField(default=0)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Account(AbstractBaseUser):
	username = models.CharField(max_length=30, unique=True)
	email = models.EmailField(verbose_name='email', max_length=60, unique=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_member = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True)
	photo = models.ImageField(upload_to='staff', default='default.jpg')
	description = models.TextField(blank=True)
	phone_regex = RegexValidator(regex=r'^\d{10}$', message="Le numéro de téléphone doit être de la forme : '0499999999'.")
	phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)
	display_email = models.BooleanField(default=True)
	display_phone_number = models.BooleanField(default=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

	objects = MyAccountManager()

	def __str__(self):
		return self.first_name + " " + self.last_name

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def order(self):
		return self.post.order
