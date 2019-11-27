# -*- encoding: utf-8 -*-

"""Определяет схемы URL для пользователей"""

from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
	# Страница входа
	url(r'^login/$', login, {'template_name': 'users/login.html', 'redirect_field_name': ''}, name='login'),
	# Страница выхода
	url(r'^logout/$', views.logout_view, name='logout'),
	# Страница регистрации
	url(r'^register/$', views.register, name='register'),
	# Активация пользователя
	url(
		r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		views.activate,
		name='activate',
	),
]
