# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Project


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
	"""Выводит один проект и все его серверы и пакеты обновлений."""
	project = Project.objects.get(id=project_id)
	servers = project.server_set.order_by('name')
	updates = project.update_set.order_by('desc')
	context = {'project': project, 'servers': servers, 'updates': updates}
	return render(request, 'ups/project.html', context)
