# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
	email = forms.EmailField(max_length=200, label='Адрес электронной почты')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
