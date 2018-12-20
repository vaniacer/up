# -*- encoding: utf-8 -*-

from .forms import ProjectForm, ServerForm, UpdateForm, ScriptEditForm, PropertiesForm, StandaloneForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Project, Server, Update, Script
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .permissions import check_perm_or404
from subprocess import check_output, call
from django.conf import settings as conf
from .commands import info, add_event
from modules.uniq import uniq
from difflib import Differ
from shutil import rmtree
from os import remove


def get_file_body(server, filename):
	command = ['ssh', server, 'cat %s' % filename]
	body = check_output(command)
	return body


def set_file_body(server, filename, body):
	command = ['ssh', server, "cat > {file} << 'EOF'\n{body}\nEOF".format(file=filename, body=body)]
	call(command)


def delete_project(project):
	"""Удаляет проект c файлами обновлений, скриптами и дампами."""
	folders = ['updates', 'scripts', 'dumps']
	home = conf.MEDIA_ROOT
	for folder in folders:
		rmtree('{home}/{folder}/{name}'.format(home=home, name=project.name, folder=folder), ignore_errors=True)
	project.delete()


def delete_server(request, server):
	"""Удаляет сервер, записывает событие в историю."""
	dick = {
		'exit': 0,
		'cron': '',
		'cdat': '',
		'serv': None,
		'uniq': uniq(),
		'proj': server.proj,
		'user': request.user,
		'name': 'Del server',
		'desc': 'Удален сервер:\n%s\n\nНазначение:\n%s' % (str(server), server.desc.encode('utf-8')),
	}
	add_event(dick)
	server.delete()


def delete_object(request, obj):
	"""Удаляет обновление\скрипт и соотв. файлы, записывает событие в историю."""
	dick = {
		'exit': 0,
		'cron': '',
		'cdat': '',
		'serv': None,
		'proj': obj.proj,
		'uniq': uniq(),
		'user': request.user,
		'name': 'Del upd\scr',
		'desc': 'Удален файл:\n%s\n\nНазначение:\n%s' % (str(obj), obj.desc.encode('utf-8')),
	}
	add_event(dick)
	remove(str(obj.file))
	obj.delete()


def edit_server_log(request, server):
	"""Записывает событие редактирования сервера в историю."""
	dick = {
		'exit': 0,
		'cron': '',
		'cdat': '',
		'serv': None,
		'uniq': uniq(),
		'proj': server.proj,
		'user': request.user,
		'name': 'Edit server',
		'desc': 'Изменен cервер:\n%s\n\nНазначение:\n%s' % (str(server), server.desc.encode('utf-8')),
	}
	add_event(dick)
	
	
def edit_object_log(request, obj, diff=''):
	"""Записывает событие редактирования обновлений\скриптов в историю."""
	dick = {
		'exit': 0,
		'cron': '',
		'cdat': '',
		'serv': None,
		'proj': obj.proj,
		'uniq': uniq(),
		'user': request.user,
		'name': 'Edit upd\scr',
		'desc': 'Изменен файл:\n{file}\n\nНазначение:\n{desc}{diff}'.format(
			desc=obj.desc.encode('utf-8'),
			file=str(obj),
			diff=diff,
		),
	}
	add_event(dick)


@login_required
def edit_project(request, project_id):
	"""Редактирует существующий проект."""
	project = get_object_or_404(Project, id=project_id)
	data = request.GET

	check_perm_or404('edit_project', project, request.user)

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

			return HttpResponseRedirect(reverse('ups:projects'))

	context = {'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_project.html', context)


@login_required
def edit_server(request, server_id):
	"""Редактирует существующий сервер."""
	server = get_object_or_404(Server, id=server_id)
	project = server.proj
	data = request.GET

	check_perm_or404('edit_server', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = ServerForm(instance=server)
	else:
		# Отправка данных POST; обработать данные.
		form = ServerForm(instance=server, data=request.POST)

		if form.is_valid():
			if request.POST.get('delete'):
				check_perm_or404('del_server', project, request.user)
				delete_server(request, server)
			elif request.POST.get('ok'):
				form.save()
				edit_server_log(request, server)

			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'server': server, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_server.html', context)


@login_required
def edit_properties(request, server_id):
	"""Редактирует jboss.properties сервера."""
	server = get_object_or_404(Server, id=server_id)
	project = server.proj
	data = request.GET
	check_perm_or404('edit_config', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		properties = get_file_body(server.addr, 'jboss.properties')
		form = PropertiesForm(initial={'properties': properties})
	else:
		# Отправка данных POST; обработать данные.
		form = PropertiesForm(request.POST)
		if form.is_valid():
			properties = form.data.get('properties').encode('utf-8')
			set_file_body(server.addr, 'jboss.properties', properties)
			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'server': server, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_properties.html', context)


@login_required
def edit_standalone(request, server_id):
	"""Редактирует standalone-full.xml сервера."""
	server = get_object_or_404(Server, id=server_id)
	project = server.proj
	data = request.GET
	check_perm_or404('edit_config', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		standalone = get_file_body(server.addr, 'jboss-bas-*/standalone/configuration/standalone-full.xml')
		form = StandaloneForm(initial={'standalone': standalone})
	else:
		# Отправка данных POST; обработать данные.
		form = StandaloneForm(request.POST)
		if form.is_valid():
			standalone = form.data.get('standalone').encode('utf-8')
			set_file_body(server.addr, 'jboss-bas-*/standalone/configuration/standalone-full.xml', standalone)
			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'server': server, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_standalone.html', context)


@login_required
def edit_update(request, update_id):
	"""Редактирует существующий пакет обновлений."""
	update = get_object_or_404(Update, id=update_id)
	project = update.proj
	data = request.GET

	check_perm_or404('edit_update', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = UpdateForm(instance=update)
	else:
		# Отправка данных POST; обработать данные.
		filename = update.file
		form = UpdateForm(request.POST, request.FILES, instance=update)

		if form.is_valid():
			if request.POST.get('delete'):
				check_perm_or404('del_update', project, request.user)
				delete_object(request, update)
			elif request.POST.get('ok'):
				if form.files:
					# если при редактировании прикладывается новый файл
					# удаляю старый чтобы не плодить файлы-призроки О_о
					remove(str(filename))

				form.save()
				edit_object_log(request, update)

			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'update': update, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_update.html', context)


@login_required
def edit_script(request, script_id):
	"""Редактирует существующий скрипт."""
	script = get_object_or_404(Script, id=script_id)
	project = script.proj
	data = request.GET

	check_perm_or404('edit_script', project, request.user)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = ScriptEditForm(instance=script)
	else:
		# Отправка данных POST; обработать данные.
		filename = script.file
		form = ScriptEditForm(request.POST, instance=script)

		if form.is_valid():
			if request.POST.get('delete'):
				check_perm_or404('del_script', project, request.user)
				delete_object(request, script)
			elif request.POST.get('ok'):
				form.save()

				with open(str(filename)) as f:
					old_text = f.readlines(1)

				new_text = script.body.replace('\r\n', '\n').encode('utf-8')
				with open(str(filename), 'wb') as f:
					f.write(new_text)

				show_difference = Differ()
				new_text = new_text.splitlines(1)
				result = list(show_difference.compare(old_text, new_text))
				diff = '\n\nИзменено:\n%s' % ''.join(result)
				edit_object_log(request, script, diff)

			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'script': script, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_script.html', context)
