# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Project, Server, Update
from django.shortcuts import render
from subprocess import call

def index(request):
	"""Домашняя страница приложения update server"""
	return render(request, 'ups/index.html')


@login_required
def projects(request):
	"""Выводит список проектов."""
	projects = Project.objects.order_by('name')
	context = {'projects': projects}
	return render(request, 'ups/projects.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы и пакеты обновлений, кнопки действий."""
	project = Project.objects.get(id=project_id)
	servers = project.server_set.order_by('name')
	updates = project.update_set.order_by('desc')

	selected_updates = request.POST.getlist('selected_updates')
	selected_servers = request.POST.getlist('selected_servers')

	SU = []
	SS = []

	if request.POST.get('select_test'):
		for id in selected_updates:
			update = Update.objects.get(id=id)
			SU.append(str(update))
		print SU

		for id in selected_servers:
			server = Server.objects.get(id=id)
			SS.append(server.addr)
		print SS

		opt = ' '.join(SS) + ' ' + ' '.join(SU)
		run = call("up/test {}" .format(opt), shell=True)
		print run

		return HttpResponseRedirect('')

	context = {'project': project, 'servers': servers, 'updates': updates}
	return render(request, 'ups/project.html', context)
