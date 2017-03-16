# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from .buttons import select_test, select_upload
from django.http import HttpResponseRedirect
from .models import Project
from django.shortcuts import render
from .permissions import check_perm


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

	if request.POST.get('select_test'):
		check_perm('run_command', current_project, request.user)
		select_test(selected_updates, selected_servers)
		return HttpResponseRedirect('')

	elif request.POST.get('select_upload'):
		check_perm('run_command', current_project, request.user)
		select_upload(selected_updates, selected_servers)
		return HttpResponseRedirect('')

	context = {'project': current_project, 'servers': servers, 'updates': updates}
	return render(request, 'ups/project.html', context)
