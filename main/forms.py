from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account


class RegistrationForm(UserCreationForm):

	class Meta:
		model = Account
		fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')
		labels = {
			"email": "Email",
			"username": "Nom d'utilisateur",
			"first_name": "Prénom",
			"last_name": "Nom de famille",
		}


class AccountAuthentificationForm(forms.ModelForm):

	password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('username', 'password')

	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(username=username, password=password):
				raise forms.ValidationError("Mauvais identifiant/mot de passe")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('photo', 'description', 'display_email', 'phone_number', 'display_phone_number')

	def clean_photo(self):
		if self.is_valid():
			photo = self.cleaned_data['photo']
			return photo

	def clean_description(self):
		if self.is_valid():
			description = self.cleaned_data['description']
			return description

	def clean_display_email(self):
		if self.is_valid():
			display_email = self.cleaned_data['display_email']
			return display_email

	def clean_phone_number(self):
		if self.is_valid():
			phone_number = self.cleaned_data['phone_number']
			return phone_number

	def clean_display_phone_number(self):
		if self.is_valid():
			display_phone_number = self.cleaned_data['display_phone_number']
			return display_phone_number
