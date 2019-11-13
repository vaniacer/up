# -*- encoding: utf-8 -*-

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render


def logout_view(request):
	"""Завершает сеанс работы с приложением."""
	logout(request)
	return HttpResponseRedirect(reverse('ups:index'))


def register(request):
	"""Регистрирует нового пользователя."""
	if request.method != 'POST':
		# Display blank registration form.
		form = UserCreationForm()
	else:
		# Обработка заполненной формы.
		form = UserCreationForm(data=request.POST)

	if form.is_valid():
		new_user = form.save()
		# Выполнение входа и перенаправление на домашнюю страницу.
		authenticated_user = authenticate(
			username=new_user.username,
			password=request.POST['password1']
		)
		login(request, authenticated_user)
		return HttpResponseRedirect(reverse('ups:index'))

	context = {'form': form}
	return render(request, 'users/register.html', context)
