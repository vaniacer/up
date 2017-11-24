# -*- encoding: utf-8 -*-

from .forms import ProjectForm, ServerForm, UpdateForm, ScriptEditForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Project, Server, Update, Script
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings as conf
from .commands_engine import add_event
from .permissions import check_perm
import shutil
import os


def delete_project(project):
	"""Удаляет проект c файлами обновлений и скриптами."""
	shutil.rmtree(conf.MEDIA_ROOT + '/updates/' + project.name, ignore_errors=True)
	shutil.rmtree(conf.MEDIA_ROOT + '/scripts/' + project.name, ignore_errors=True)
	project.delete()


def delete_server(request, server):
	"""Удаляет сервер, записывает событие в историю."""
	dick = {'project': server.proj, 'user': request.user, 'command': 'Del server'}
	add_event(dick, 'Удален сервер:\n%s\n\nНазначение:\n%s' % (str(server), server.desc.encode('utf-8')), 0, '', '')
	server.delete()


def delete_object(request, obj):
	"""Удаляет обновление\скрипт и соотв. файлы, записывает событие в историю."""
	dick = {'project': obj.proj, 'user': request.user, 'command': 'Del upd\scr'}
	add_event(dick, 'Удален файл:\n%s\n\nНазначение:\n%s' % (str(obj), obj.desc.encode('utf-8')), 0, '', '')
	os.remove(str(obj.file))
	obj.delete()


def edit_object(request, obj):
	"""Записывает событие редактирования в историю."""
	dick = {'project': obj.proj, 'user': request.user, 'command': 'Edit upd\scr'}
	add_event(dick, 'Изменен файл:\n%s\n\nНазначение:\n%s' % (str(obj), obj.desc.encode('utf-8')), 0, '', '')


@login_required
def edit_project(request, project_id):
	"""Редактирует существующий проект."""
	# project = Project.objects.get(id=project_id)
	project = get_object_or_404(Project, id=project_id)

	check_perm('edit_project', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = ProjectForm(instance=project)
	else:
		# Отправка данных POST; обработать данные.
		form = ProjectForm(instance=project, data=request.POST)

		if form.is_valid():
			if request.POST.get('delete'):
				delete_project(project)
				return HttpResponseRedirect(reverse('ups:projects'))
			elif request.POST.get('ok'):
				form.save()

			return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/edit_project.html', context)


@login_required
def edit_server(request, server_id):
	"""Редактирует существующий сервер."""
	# server = Server.objects.get(id=server_id)
	server = get_object_or_404(Server, id=server_id)
	project = server.proj

	check_perm('edit_server', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = ServerForm(instance=server)
	else:
		# Отправка данных POST; обработать данные.
		form = ServerForm(instance=server, data=request.POST)

		if form.is_valid():
			if request.POST.get('delete'):
				check_perm('del_server', project, request.user)
				delete_server(request, server)
			elif request.POST.get('ok'):
				form.save()

			return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'server': server, 'project': project, 'form': form}
	return render(request, 'ups/edit_server.html', context)


@login_required
def edit_update(request, update_id):
	"""Редактирует существующий пакет обновлений."""
	# update = Update.objects.get(id=update_id)
	update = get_object_or_404(Update, id=update_id)
	project = update.proj

	check_perm('edit_update', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = UpdateForm(instance=update)
	else:
		# Отправка данных POST; обработать данные.
		filename = update.file
		form = UpdateForm(request.POST, request.FILES, instance=update)

		if form.is_valid():
			if request.POST.get('delete'):
				check_perm('del_update', project, request.user)
				delete_object(request, update)
			elif request.POST.get('ok'):
				if form.files:
					# если при редактировании прикладывается новый файл
					# удаляю старый чтобы не плодить файлы-призроки О_о
					os.remove(str(filename))

				form.save()
				edit_object(request, update)

			return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'update': update, 'project': project, 'form': form}
	return render(request, 'ups/edit_update.html', context)


@login_required
def edit_script(request, script_id):
	"""Редактирует существующий скрипт."""
	script = get_object_or_404(Script, id=script_id)
	project = script.proj

	check_perm('edit_script', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = ScriptEditForm(instance=script)
	else:
		# Отправка данных POST; обработать данные.
		filename = script.file
		form = ScriptEditForm(request.POST, instance=script)

		if form.is_valid():
			if request.POST.get('delete'):
				check_perm('del_update', project, request.user)
				delete_object(request, script)
			elif request.POST.get('ok'):
				form.save()
				body = open(str(filename), 'wb')
				body.write(script.body.replace('\r\n', '\n'))
				body.close()
				edit_object(request, script)

			return HttpResponseRedirect(reverse('ups:project', args=[project.id]))

	context = {'script': script, 'project': project, 'form': form}
	return render(request, 'ups/edit_script.html', context)
