# -*- encoding: utf-8 -*-

"""Определяет схемы URL для update server'a."""

from . import views, views_new, views_edit
from django.conf.urls import url

urlpatterns = [
	# Домашняя страница
	url(r'^$', views.index, name='index'),

	# Пользовательские настройки.
	url(r'^profile/$', views_edit.edit_profile, name='profile'),

	# Отмена команды.
	url(r'^cancel/$', views.cancel, name='cancel'),
	# Страница логов.
	url(r'^command_log/$', views.command_log, name='command_log'),
	# Страница минилогов.
	url(r'^mini_log/$', views.mini_log, name='mini_log'),

	# Вывод всех проектов.
	url(r'^projects/$', views.projects, name='projects'),
	# Страница для добавления нового проекта
	url(r'^new_project/$', views_new.new_project, name='new_project'),
	# Страница истории проекта
	url(r'^history/(?P<project_id>\d+)/$', views.history_view, name='history'),
	# Страница с подробной информацией по отдельному проекту
	url(r'^projects/(?P<project_id>\d+)/$', views.project_view, name='project'),
	# Страница для редактирования проекта
	url(r'^edit_project/(?P<project_id>\d+)/$', views_edit.edit_project, name='edit_project'),

	# Страница для добавления нового сервера
	url(r'^new_server/(?P<project_id>\d+)/$', views_new.new_server, name='new_server'),
	# Страница для редактирования сервера
	url(r'^edit_server/(?P<server_id>\d+)/$', views_edit.edit_server, name='edit_server'),
	# Страница для редактирования jboss.properties файла сервера
	url(r'^edit_properties/(?P<server_id>\d+)/$', views_edit.edit_properties, name='edit_properties'),
	# Страница для редактирования standalone-full.xml файла сервера
	url(r'^edit_standalone/(?P<server_id>\d+)/$', views_edit.edit_standalone, name='edit_standalone'),

	# Страница тунелирования
	url(r'^tunnel/(?P<server_id>\d+)/$', views_edit.tunnel, name='tunnel'),
	# Страница добавления к ЕТВ
	url(r'^idp/(?P<project_id>\d+)/$', views_edit.idp, name='idp'),

	# Страница для добавления нового обновления
	url(r'^new_update/(?P<project_id>\d+)/$', views_new.upload_update, name='new_update'),
	# Страница для редактирования обновления
	url(r'^edit_update/(?P<update_id>\d+)/$', views_edit.edit_update, name='edit_update'),
	# Скачать файл обновления.
	url(r'^download_upd/(?P<project_id>\d+)/(?P<update_id>\d+)$', views.download_upd, name='download_upd'),

	# Страница для добавления нового скрипта
	url(r'^add_script/(?P<project_id>\d+)/$', views_new.upload_script, name='add_script'),
	# Страница для создания скрипта
	url(r'^new_script/(?P<project_id>\d+)/$', views_new.create_script, name='new_script'),
	# Страница для редактирования скрипта
	url(r'^edit_script/(?P<script_id>\d+)/$', views_edit.edit_script, name='edit_script'),
	# Скачать файл скрипта.
	url(r'^download_script/(?P<project_id>\d+)/(?P<script_id>\d+)$', views.download_script, name='download_script'),

	# Скачать файл дампа базы.
	url(r'^download_dump/(?P<project_id>\d+)/(?P<dump>.+)$', views.download_dump, name='download_dump'),
	# Страница для добавления дампа
	url(r'^add_dump/(?P<project_id>\d+)/$', views_new.upload_dump, name='add_dump'),
]
