# -*- encoding: utf-8 -*-

from .forms import ProjectForm, ServerForm, UpdateForm, ScriptAddForm, ScriptCreateForm, DumpForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .permissions import check_perm_or404
from django.conf import settings as conf
from os.path import isfile, splitext
from django.shortcuts import render
from modules.uniq import uniq
from .models import Project
from .commands import info
from os import remove


def handle_uploaded_dump(dump_file, projectname):
	filename = str(dump_file)
	filepath = '{home}/dumps/{project}/{file}'.format(
		home=conf.MEDIA_ROOT,
		project=projectname,
		file=filename,
	)
	if isfile(filepath):
		filename, extension = splitext(filepath)
		filepath = '{old}_{key}{ext}'.format(old=filename, key=uniq(), ext=extension)

	with open(filepath, 'wb+') as destination:
		for chunk in dump_file.chunks():
			destination.write(chunk)


# @login_required
@permission_required('ups.add_project')
def new_project(request):
	"""Определяет новый проект."""
	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ProjectForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ProjectForm(request.POST)

		if form.is_valid():
			project = form.save(commit=False)
			project.user = request.user
			form.save()
			return HttpResponseRedirect(reverse('ups:projects'))

	context = {'form': form}
	return render(request, 'ups/new_project.html', context)


@login_required
def new_server(request, project_id):
	"""Добавляет новый сервер."""
	project = Project.objects.get(id=project_id)
	check_perm_or404('add_server', project, request.user)
	data = request.GET

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ServerForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ServerForm(data=request.POST)

		if form.is_valid():
			server = form.save(commit=False)
			server.user = request.user
			server.proj = project
			server.save()
			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/new_server.html', context)


@login_required
def upload_update(request, project_id):
	"""Добавляет новое обновление."""
	project = Project.objects.get(id=project_id)
	check_perm_or404('add_update', project, request.user)
	data = request.GET

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = UpdateForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = UpdateForm(request.POST, request.FILES)

		if form.is_valid():
			update = form.save(commit=False)
			update.flnm = update.file.name.split('/')[-1]
			update.user = request.user
			update.proj = project
			update.save()
			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/new_update.html', context)


@login_required
def upload_dump(request, project_id):
	"""Загружает новое обновление."""
	project = Project.objects.get(id=project_id)
	check_perm_or404('run_dump', project, request.user)
	data = request.GET

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = DumpForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = DumpForm(request.POST, request.FILES)

		if form.is_valid():
			handle_uploaded_dump(request.FILES['file'], project.name)
			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/new_dump.html', context)


@login_required
def upload_script(request, project_id):
	"""Загружает новый скрипт."""
	project = Project.objects.get(id=project_id)
	check_perm_or404('add_script', project, request.user)
	data = request.GET

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ScriptAddForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ScriptAddForm(request.POST, request.FILES)

		if form.is_valid():
			script = form.save(commit=False)
			# Check permission to upload this type of scripts, this also prevent attempts to add unknown script types
			perm = u'add_{type}'.format(type=script.file.name.split('.')[-1])
			check_perm_or404(perm, project, request.user)

			script.user = request.user
			script.proj = project
			script.save()

			with open(str(script.file), 'rU') as f:
				script.body = f.read()
			script.flnm = script.file.name.split('/')[-1]
			try:
				script.save()
			except ValueError:
				script.delete()
				remove(str(script.file))
				return render(request, 'ups/500.html', {'error': 'Encoding not supported.'})

			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/new_script.html', context)


@login_required
def create_script(request, project_id):
	"""Создает новый скрипт."""
	project = Project.objects.get(id=project_id)
	check_perm_or404('add_script', project, request.user)
	data = request.GET

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ScriptCreateForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ScriptCreateForm(request.POST)

		if form.is_valid():
			script = form.save(commit=False)
			# Check permission to create this type of scripts, this also prevent attempts to add unknown script types
			perm = u'add_{type}'.format(type=script.flnm.split('.')[-1])
			check_perm_or404(perm, project, request.user)
			new_file = ContentFile(script.body.replace('\r\n', '\n').encode('utf-8'))
			new_file.name = script.flnm
			script.user = request.user
			script.file = new_file
			script.proj = project
			script.save()

			return HttpResponseRedirect('/projects/%s/?%s' % (project.id, info(data)))

	context = {'project': project, 'form': form, 'info': info(data)}
	return render(request, 'ups/create_script.html', context)
