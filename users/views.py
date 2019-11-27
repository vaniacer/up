# -*- encoding: utf-8 -*-

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.shortcuts import render
from .forms import SignupForm


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
			mail_subject = 'UpS account activation'
			message = render_to_string('users/activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			context = {'mess': 'Please confirm your email address to complete the registration.'}
			return render(request, 'users/after_register.html', context)
	else:
		form = SignupForm()

	context = {'form': form}
	return render(request, 'users/register.html', context)


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		context = {'mess': 'Thank you for your email confirmation. Now you can login to your account.'}
	else:
		context = {'mess': 'Activation link is invalid!'}
	return render(request, 'users/after_register.html', context)
