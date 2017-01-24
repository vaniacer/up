# -*- encoding: utf-8 -*-

from django.shortcuts import render
from .models import Project, Server

def index(request):
	"""Домашняя страница приложения Learning Log"""
	return render(request, 'ups/index.html')


def projects(request):
	"""Выводит список проектов."""
	projects = Project.objects.order_by('name')
	context = {'projects': projects}
	return render(request, 'ups/projects.html', context)


def project(request, project_id):
	"""Выводит один проект и все его серверы."""
	project = Project.objects.get(id=project_id)
	servers = project.server_set.order_by('name')
	context = {'project': project, 'servers': servers}
	return render(request, 'ups/project.html', context)