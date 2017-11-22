# -*- encoding: utf-8 -*-

"""Определяет схемы URL для update server'a."""

from . import views, views_new, views_edit
from django.conf.urls import url

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
	# Страница для добавления нового скрипта
	url(r'^new_script/(?P<project_id>\d+)/$', views_new.new_script, name='new_script'),
	# Страница для редактирования проекта
	url(r'^edit_project/(?P<project_id>\d+)/$', views_edit.edit_project, name='edit_project'),
	# Страница для редактирования сервера
	url(r'^edit_server/(?P<server_id>\d+)/$', views_edit.edit_server, name='edit_server'),
	# Страница для редактирования обновления
	url(r'^edit_update/(?P<update_id>\d+)/$', views_edit.edit_update, name='edit_update'),
	# Страница для редактирования скрипта
	url(r'^edit_script/(?P<script_id>\d+)/$', views_edit.edit_script, name='edit_script'),
	# Отмена команды.
	url(r'^cancel/(?P<project_id>\d+)/(?P<pid>\d+)/(?P<cmd>\w+)/(?P<log_id>\w+)/$', views.cancel, name='cancel'),
	# Скачать файл скрипта.
	url(r'^download_script/(?P<project_id>\d+)/(?P<script_id>\d+)$', views.download_script, name='download_script'),
	# Скачать файл обновления.
	url(r'^download_upd/(?P<project_id>\d+)/(?P<update_id>\d+)$', views.download_upd, name='download_upd'),
	# Скачать dump.
	url(r'^download_dump/(?P<project_id>\d+)/(?P<dump>.+)$', views.download_dump, name='download_dump'),
	# Вывод логов.
	url(
		r'^logs/(?P<project_id>\w+)/(?P<log_id>\w+)/(?P<cmd>\w+)/(?P<cron>\w+)/(?P<date>\w+)/$',
		views.logs,
		name='logs'),
]
