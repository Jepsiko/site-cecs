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
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not authenticate(username=username, password=password):
			raise forms.ValidationError("Mauvais identifiant/mot de passe")
