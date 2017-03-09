# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ServerForm, UpdateForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Project, Server, Update
from django.shortcuts import render
from .groups import delete_groups
import shutil
import os


def delete_project(project):
	"""Удаляет проект, группы и файлы обновлений."""
	shutil.rmtree("up/media/updates/{}" .format(project.name))
	delete_groups(project)
	project.delete()


def delete_update(update):
	"""Удаляет обновление и файлы обновлений."""
	os.remove("up/media/{}" .format(update.update))
	update.delete()


@login_required
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
			if request.POST.get('delete'):
				delete_project(project)
				return HttpResponseRedirect(reverse('ups:projects'))
			else:
				return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/edit_project.html', context)


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
			if request.POST.get('delete'):
				server.delete()
			return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'server': server, 'project': project, 'form': form}
	return render(request, 'ups/edit_server.html', context)


@login_required
def edit_update(request, update_id):
	"""Редактирует существующий пакет обновлений."""
	update = Update.objects.get(id=update_id)
	project = update.project

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = UpdateForm(instance=update)
	else:
		# Отправка данных POST; обработать данные.
		form = UpdateForm(request.POST, request.FILES, instance=update)

		if form.is_valid():
			form.save()
			if request.POST.get('delete'):
				delete_update(update)
			return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'update': update, 'project': project, 'form': form}
	return render(request, 'ups/edit_update.html', context)
