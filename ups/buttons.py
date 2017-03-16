# -*- encoding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Server, Update
from subprocess import call


def make_lists(selected_updates, selected_servers):
	"""Создает списки избранных серверов и апдейтов."""

	updates = []
	servers = []

	for i in selected_updates:
		updates.append(Update.objects.get(id=i))

	for i in selected_servers:
		servers.append(Server.objects.get(id=i))

	print updates, '\n', servers
	return [servers, updates]


def select_test(selected_updates, selected_servers):
	"""Обрабатывает событие select_test."""

	selected = make_lists(selected_updates, selected_servers)
	servers = selected[0]
	updates = selected[1]

	opt = ' '.join(str(u) for u in updates) + ' ' + ' '.join(str(s.addr) for s in servers)
	run = call("bash/test {}".format(opt), shell=True)
	print run


def select_upload(selected_updates, selected_servers):
	"""Обрабатывает событие select_upload."""

	selected = make_lists(selected_updates, selected_servers)
	servers = selected[0]
	updates = selected[1]

	for s in servers:
		opt = str(s.addr) + ' ' + str(s.wdir) + ' ' + ' '.join('media/' + str(u.file) for u in updates)
		run = call("bash/copy {}".format(opt), shell=True)
		print run


def buttons(request):
	"""Обрабатывает кнопки."""

	# Selected objects ID's.
	selected_updates = request.POST.getlist('selected_updates')
	selected_servers = request.POST.getlist('selected_servers')

	if request.POST.get('select_test'):
		select_test(selected_updates, selected_servers)

	elif request.POST.get('select_upload'):
		select_upload(selected_updates, selected_servers)

	return HttpResponseRedirect('')

