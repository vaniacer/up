# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Project, Server, Update
from django.shortcuts import render
from .permissions import check_perm
from subprocess import call


def index(request):
	"""Домашняя страница приложения update server"""
	return render(request, 'ups/index.html')


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и обрабатывает кнопки действий."""
	current_project = Project.objects.get(id=project_id)

	check_perm('view_project', current_project, request.user)

	servers = current_project.server_set.order_by('name')
	updates = current_project.update_set.order_by('date').reverse()

	selected_updates = request.POST.getlist('selected_updates')
	selected_servers = request.POST.getlist('selected_servers')

	su = []
	ss = []

	if request.POST.get('select_test'):

		check_perm('run_command', current_project, request.user)

		for i in selected_updates:
			update = Update.objects.get(id=i)
			su.append(str(update))
		print su

		for i in selected_servers:
			server = Server.objects.get(id=i)
			ss.append(server.addr)
		print ss

		opt = ' '.join(ss) + ' ' + ' '.join(su)
		run = call("up/bash/test {}" .format(opt), shell=True)
		print run

		return HttpResponseRedirect('')
	elif request.POST.get('cancel'):
		return HttpResponseRedirect(reverse('ups:projects'))

	context = {'project': current_project, 'servers': servers, 'updates': updates}
	return render(request, 'ups/project.html', context)
