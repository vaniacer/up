# -*- encoding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms  import ProjectForm, ServerForm
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


def new_project(request):
	"""Определяет новый проект."""
	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ProjectForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ProjectForm(request.POST)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('ups:projects'))

	context = {'form': form}
	return render(request, 'ups/new_project.html', context)


def new_server(request, project_id):
	"""Добавляет новый сервер."""
	project = Project.objects.get(id=project_id)

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ServerForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ServerForm(data=request.POST)

	if form.is_valid():
		new_server = form.save(commit=False)
		new_server.project = project
		new_server.save()
		return HttpResponseRedirect(reverse('ups:project', args=[project_id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/new_server.html', context)


def edit_server(request, server_id):
	"""Редактирует существующий сервер."""
	server = Server.objects.get(id=server_id)
	project = server.project

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = ServerForm(instance=server)
	else:
		# Отправка данных POST; обработать данные.
		form = ServerForm(instance=server, data=request.POST)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'server': server, 'project': project, 'form': form}
	return render(request, 'ups/edit_server.html', context)


def edit_project(request, project_id):
	"""Редактирует существующий проект."""
	project = Project.objects.get(id=project_id)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = ProjectForm(instance=project)
	else:
		# Отправка данных POST; обработать данные.
		form = ProjectForm(instance=project, data=request.POST)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/edit_project.html', context)