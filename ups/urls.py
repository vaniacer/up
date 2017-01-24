# -*- encoding: utf-8 -*-

"""Определяет схемы URL для learning_logs."""

from django.conf.urls import url
from . import views

urlpatterns = [
	# Домашняя страница
	url(r'^$', views.index, name='index'),
	# Вывод всех проектов.
	url(r'^projects/$', views.projects, name='projects'),
	# Страница с подробной информацией по отдельному проекту
	url(r'^projects/(?P<project_id>\d+)/$', views.project, name='project'),
	# Страница для добавления нового проекта
	url(r'^new_project/$', views.new_project, name='new_project'),
	# Страница для добавления нового сервера
	url(r'^new_server/(?P<project_id>\d+)/$', views.new_server, name='new_server'),
]