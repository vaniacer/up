# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from .forms  import ProjectForm, ServerForm
from django.shortcuts import render
from .models import Project, Server

groups = ('view', 'dump', 'updt', 'upld')

def create_groups(project):
	"""Создает группы для каждого нового проекта."""
	for group in groups:
		Group.objects.get_or_create(name=project + '_' + group)


def check_groups(project):
	"""Подключает созанные группы к проекту."""
	names = {}
	if project.view.name == 'dummy':
		for group in groups:
			name = {group: project.name + '_' + group}
			names.update(name)
		print names


def index(request):
	"""Домашняя страница приложения Learning Log"""
	return render(request, 'ups/index.html')


@login_required
def projects(request):
	"""Выводит список проектов."""
	projects = Project.objects.order_by('name')
	context = {'projects': projects}
	return render(request, 'ups/projects.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект и все его серверы."""
	project = Project.objects.get(id=project_id)
	servers = project.server_set.order_by('name')
	context = {'project': project, 'servers': servers}
	return render(request, 'ups/project.html', context)


@login_required
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
		create_groups(request.POST['name'])
		return HttpResponseRedirect(reverse('ups:projects'))

	context = {'form': form}
	return render(request, 'ups/new_project.html', context)


@login_required
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


@login_required
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


@login_required
def edit_project(request, project_id):
	"""Редактирует существующий проект."""
	project = Project.objects.get(id=project_id)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		check_groups(project)
		form = ProjectForm(instance=project)
	else:
		# Отправка данных POST; обработать данные.
		form = ProjectForm(instance=project, data=request.POST)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/edit_project.html', context)