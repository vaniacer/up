# -*- encoding: utf-8 -*-

"""Определяет схемы URL для update server'a."""

from django.conf.urls import url
from . import views, views_new, views_edit
from django.contrib.auth.views import login


urlpatterns = [
	# Домашняя страница
	url(r'^$', views.index, name='index'),
	# Вывод всех проектов.
	url(r'^projects/$', views.projects, name='projects'),
	# Страница с подробной информацией по отдельному проекту
	url(r'^projects/(?P<project_id>\d+)/$', views.project, name='project'),
	# Страница для добавления нового проекта
	url(r'^new_project/$', views_new.new_project, name='new_project'),
	# Страница для добавления нового сервера
	url(r'^new_server/(?P<project_id>\d+)/$', views_new.new_server, name='new_server'),
	# Страница для добавления нового обновления
	url(r'^new_update/(?P<project_id>\d+)/$', views_new.new_update, name='new_update'),
	# Страница для редактирования проекта
	url(r'^edit_project/(?P<project_id>\d+)/$', views_edit.edit_project, name='edit_project'),
	# Страница для редактирования сервера
	url(r'^edit_server/(?P<server_id>\d+)/$', views_edit.edit_server, name='edit_server'),
	# Страница для редактирования обновления
	url(r'^edit_update/(?P<update_id>\d+)/$', views_edit.edit_update, name='edit_update'),
	# Вывод логов.
	url(r'^logs/(?P<project_id>\w+)/(?P<log_id>\w+)/(?P<cmd>\w+)/$', views.logs, name='logs'),
]
