# -*- encoding: utf-8 -*-

from .forms import ProjectForm, ServerForm, UpdateForm, ScriptEditForm, PropertiesForm, StandaloneForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Project, Server, Update, Script
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .permissions import check_perm_or404
from django.conf import settings as conf
from .commands import info, add_event
from difflib import unified_diff
from up.settings import TMP_DIR
from os.path import join as opj
from modules.uniq import uniq
from subprocess import call
from shutil import rmtree
from os import remove


def get_file(server, source, destination):
	"""Читает тело файла, возвращает ошибку и тело."""
	file_body = ''
	command = ['rsync', '-gzort', '{server}:{source}'.format(
		source=source,
		server=server,
	), destination]

	error = call(command)

	if not error:
		with open(destination, 'r') as f:
			file_body = f.read()
			remove(destination)

	return error, file_body


def send_file(server, filename, destination, text):
	"""Записывает текст в файл, отправляет файл по адресу"""
	with open(filename, 'w') as f:
		f.write(text)

	command = ['rsync', '--remove-source-files', '-gzort', filename, '{server}:{dest}'.format(
		dest=destination,
		file=filename,
		server=server,
	)]
	call(command)


def log_diff(request, server, confname, old_text, new_text):
	"""Создает запись в истории о изменении в конфайле."""
	result = unified_diff(old_text.splitlines(True), new_text.splitlines(True))
	diff = 'Изменено:\n{}'.format(''.join(result))
	diff = diff.replace('<', '&lt;')
	diff = diff.replace('>', '&gt;')
	edit_conf(request, server, confname, diff)


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
		'http': '',
		'serv': None,
		'cjob': False,
		'uniq': uniq(),
		'proj': server.proj,
		'user': request.user,
		'name': 'Del server',
		'desc': 'Удален сервер:\n%s\n\nНазначение:\n%s' % (str(server), server.desc.encode('utf-8')),
	}
	add_event(dick)
	server.delete()


def delete_object(request, obj):
	"""Удаляет обновление или скрипт и соотв. файлы, записывает событие в историю."""
	dick = {
		'exit': 0,
		'cron': '',
		'cdat': '',
		'http': '',
		'serv': None,
		'cjob': False,
		'uniq': uniq(),
		'proj': obj.proj,
		'user': request.user,
		'name': 'Del update or script',
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
		'http': '',
		'serv': None,
		'cjob': False,
		'uniq': uniq(),
		'proj': server.proj,
		'user': request.user,
		'name': 'Edit server',
		'desc': 'Изменен cервер:\n%s\n\nНазначение:\n%s' % (str(server), server.desc.encode('utf-8')),
	}
	add_event(dick)


def edit_object_log(request, obj, diff=''):
	"""Записывает событие редактирования обновлений или скриптов в историю."""
	dick = {
		'exit': 0,
		'cron': '',
		'cdat': '',
		'http': '',
		'serv': None,
		'cjob': False,
		'uniq': uniq(),
		'proj': obj.proj,
		'user': request.user,
		'name': 'Edit upd\scr',
		'desc': 'Изменен файл:\n{file}\n\nНазначение:\n{desc}{diff}'.format(
			desc=obj.desc.encode('utf-8'),
			file=str(obj),
			diff=diff,
		),
	}
	add_event(dick)


def edit_conf(request, server, confile, diff=''):
	"""Записывает событие редактирования обновлений или скриптов в историю."""
	dick = {
		'exit': 0,
		'cron': '',
		'cdat': '',
		'http': '',
		'desc': diff,
		'serv': None,
		'cjob': False,
		'uniq': uniq(),
		'proj': server.proj,
		'user': request.user,
		'name': 'Edit {conf} on server {server}'.format(conf=confile, server=server),
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

			return HttpResponseRedirect(u'/projects/%s/?%s' % (project.id, info(data)))

	context = {'server': server, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_server.html', context)


@login_required
def tunnel(request, server_id):
	"""Создает тунель на сервер."""
	server = get_object_or_404(Server, id=server_id)
	project = server.proj
	data = request.GET
	check_perm_or404('tunnel', project, request.user)

	if data.get('port'):
		port = data.get('port')
		opts = request.META['HTTP_REFERER']
		opts = opts.split('?')[1]

		url = u'/projects/{pid}/?run_type=RUN&run_cmnd=tunnel&selected_servers={sid}&port={port}{opts}'.format(
			pid=project.id, sid=server_id, port=port, opts=opts)
		return HttpResponseRedirect(url)

	context = {'server': server, 'project': project, 'port': server.port, 'info': info(data)}
	return render(request, 'ups/tunnel.html', context)


@login_required
def idp(request, project_id):
	"""Подключает нового клиента к ЕТВ"""
	project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', project, request.user)
	check_perm_or404('connect_to_idp', project, request.user)

	idprojects = Project.objects.order_by('name')
	idprojects = [P.name for P in idprojects]

	data = request.GET
	addr = data.get('addr') or ''
	name = data.get('name') or ''
	prod = data.get('prod') or ''
	urli = data.get('info') or info(data)
	path = data.get('path') or '/var/lib/jboss/idp'
	servers = data.getlist('selected_servers')
	context = {
		'idprojects': idprojects,
		'servers': servers,
		'project': project,
		'addr': addr,
		'path': path,
		'name': name,
		'info': urli
	}

	if prod:
		idprod = get_object_or_404(Project, name=prod)
		idpsrv = idprod.server_set.order_by('name')
		idpsrv = [{'name': S.name, 'addr': S.addr} for S in idpsrv]
		context['idp_servers'] = idpsrv
		context['prod'] = prod

	if addr and name and path:
		opts = '&selected_dbdumps={A}&selected_dbdumps={P}&selected_dbdumps={N}'.format(A=addr, N=name, P=path)
		servers = ['&selected_servers={S}'.format(S=server) for server in servers]
		servers = ''.join(servers)
		url = u'/projects/{pid}/?run_type=RUN&run_cmnd=connect_to_idp{servers}{opts}{info}'.format(
			pid=project.id, servers=servers, opts=opts, info=urli)
		return HttpResponseRedirect(url)

	return render(request, 'ups/idp.html', context)


@login_required
def edit_properties(request, server_id):
	"""Редактирует jboss.properties сервера."""
	server = get_object_or_404(Server, id=server_id)
	project = server.proj
	data = request.GET
	check_perm_or404('edit_config', project, request.user)
	confname = 'jboss.properties'
	filename = opj(TMP_DIR, 'properties{}'.format(uniq()))
	destination = '{wdir}/{conf}'.format(wdir=server.wdir, conf=confname)

	error, properties_old = get_file(server.addr, destination, filename)
	if error:
		context = {'server': server, 'project': project, 'info': info(data)}
		return render(request, 'ups/server_unreachable.html', context)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = PropertiesForm(initial={'properties': properties_old})
	else:
		# Отправка данных POST; обработать данные.
		form = PropertiesForm(request.POST)
		if form.is_valid():
			properties_new = form.data.get('properties').encode('utf-8')
			send_file(server.addr, filename, destination, properties_new)
			log_diff(request, server, confname, properties_old, properties_new)
			return HttpResponseRedirect(u'/projects/{id}/?{opts}'.format(id=project.id, opts=info(data)))

	context = {'server': server, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_properties.html', context)


@login_required
def edit_standalone(request, server_id):
	"""Редактирует standalone-full.xml сервера."""
	server = get_object_or_404(Server, id=server_id)
	project = server.proj
	data = request.GET
	check_perm_or404('edit_config', project, request.user)
	confname = 'standalone-full.xml'
	filename = opj(TMP_DIR, 'standalone{}'.format(uniq()))
	destination = '{wdir}/jboss-bas-*/standalone/configuration/{conf}'.format(wdir=server.wdir, conf=confname)

	error, standalone_old = get_file(server.addr, destination, filename)
	if error:
		context = {'server': server, 'project': project, 'info': info(data)}
		return render(request, 'ups/server_unreachable.html', context)

	if request.method != 'POST':
		# Исходный запрос; форма заполняется данными текущей записи.
		form = StandaloneForm(initial={'standalone': standalone_old})
	else:
		# Отправка данных POST; обработать данные.
		form = StandaloneForm(request.POST)
		if form.is_valid():
			standalone_new = form.data.get('standalone').encode('utf-8')
			send_file(server.addr, filename, destination, standalone_new)
			log_diff(request, server, confname, standalone_old, standalone_new)
			return HttpResponseRedirect(u'/projects/{id}/?{opts}'.format(id=project.id, opts=info(data)))

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

			return HttpResponseRedirect(u'/projects/%s/?%s' % (project.id, info(data)))

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
					old_text = f.readlines(True)

				new_text = script.body.replace('\r\n', '\n').encode('utf-8')
				with open(str(filename), 'wb') as f:
					f.write(new_text)

				new_text = new_text.splitlines(True)
				result = unified_diff(old_text, new_text)
				diff = '\n\nИзменено:\n%s' % ''.join(result)
				edit_object_log(request, script, diff)

			return HttpResponseRedirect(u'/projects/%s/?%s' % (project.id, info(data)))

	context = {'script': script, 'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/edit_script.html', context)
