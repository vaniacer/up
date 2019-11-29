# -*- encoding: utf-8 -*-

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from .forms import SignupForm


def get_object_or_false(func):
	def wrapper(*args, **kwargs):
		try:
			obj = func(*args, **kwargs)
			return obj
		except:
			return False
	return wrapper


get_object_or_404 = get_object_or_false(get_object_or_404)


def logout_view(request):
	"""Завершает сеанс работы с приложением."""
	logout(request)
	return HttpResponseRedirect(reverse('users:login'))


def register(request):
	"""Регистрирует нового пользователя."""
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'UpS account activation'
			message = render_to_string('users/activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			toadr = form.cleaned_data.get('email')
			email = EmailMessage(subject, message, to=[toadr])
			email.send()
			context = {'mess': 'Please confirm your email address to complete the registration.'}
			return render(request, 'users/after_register.html', context)
	else:
		form = SignupForm()

	context = {'form': form}
	return render(request, 'users/register.html', context)


def activate(request, uidb64, token):
	uid = force_text(urlsafe_base64_decode(uidb64))
	context = {'mess': "You've done a bad thing!"}
	user = get_object_or_404(User, pk=uid)
	if user:
		check = account_activation_token.check_token(user, token)
		if check:
			user.is_active = True
			user.save()
			context = {'mess': 'Email confirmed. Now you can login to your account.'}
	return render(request, 'users/after_register.html', context)
