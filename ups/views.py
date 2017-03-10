# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from .models import Project, Server, Update
from .permissions import check_view_perm
from django.shortcuts import render
from subprocess import call


def index(request):
	"""Домашняя страница приложения update server"""
	print request.user.get_all_permissions()
	# print request.user.has_perm('view_project', test1)
	return render(request, 'ups/index.html')


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	for p in project_list:
		print request.user.has_perm('view_project', p)
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


# @login_required
@permission_required('ups.view_project')
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и обрабатывает кнопки действий."""
	current_project = Project.objects.get(id=project_id)

	# check_view_perm(current_project, request.user)

	servers = current_project.server_set.order_by('name')
	updates = current_project.update_set.order_by('desc')

	selected_updates = request.POST.getlist('selected_updates')
	selected_servers = request.POST.getlist('selected_servers')

	su = []
	ss = []

	if request.POST.get('select_test'):
		for i in selected_updates:
			update = Update.objects.get(id=i)
			su.append(str(update))
		print su

		for i in selected_servers:
			server = Server.objects.get(id=i)
			ss.append(server.addr)
		print ss

		opt = ' '.join(ss) + ' ' + ' '.join(su)
		run = call("up/test {}" .format(opt), shell=True)
		print run

		return HttpResponseRedirect('')

	context = {'project': current_project, 'servers': servers, 'updates': updates}
	return render(request, 'ups/project.html', context)
