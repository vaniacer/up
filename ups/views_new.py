# -*- encoding: utf-8 -*-

from .forms import ProjectForm, ServerForm, UpdateForm, ScriptAddForm, ScriptCreateForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .permissions import check_perm
from .models import Project
from django.conf import settings as conf


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
	check_perm('add_server', project, request.user)

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
			return HttpResponseRedirect(reverse('ups:project', args=[project_id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/new_server.html', context)


@login_required
def new_update(request, project_id):
	"""Добавляет новое обновление."""
	project = Project.objects.get(id=project_id)
	check_perm('add_update', project, request.user)

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = UpdateForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = UpdateForm(request.POST, request.FILES)

		if form.is_valid():
			update = form.save(commit=False)
			update.user = request.user
			update.proj = project
			update.save()
			return HttpResponseRedirect(reverse('ups:project', args=[project_id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/new_update.html', context)


@login_required
def new_script(request, project_id):
	"""Добавляет новый скрипт."""
	project = Project.objects.get(id=project_id)
	check_perm('add_script', project, request.user)

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ScriptAddForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ScriptAddForm(request.POST, request.FILES)

		if form.is_valid():
			script = form.save(commit=False)
			script.user = request.user
			script.proj = project
			script.save()

			body = open(str(script.file), 'rU')
			script.body = body.read()
			body.close()
			script.save()

			return HttpResponseRedirect(reverse('ups:project', args=[project_id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/new_script.html', context)


@login_required
def create_script(request, project_id):
	"""Создает новый скрипт."""
	project = Project.objects.get(id=project_id)
	check_perm('add_script', project, request.user)

	if request.method != 'POST':
		# Данные не отправлялись; создается пустая форма.
		form = ScriptCreateForm()
	else:
		# Отправлены данные POST; обработать данные.
		form = ScriptCreateForm(request.POST)

		if form.is_valid():
			script = form.save(commit=False)
			script.file = '%s/scripts/%s/%s' % (conf.MEDIA_ROOT, project.name, script.flnm)
			script.user = request.user
			script.proj = project

			body = open(str(script.file), 'wb')
			body.write(script.body.replace('\r\n', '\n').encode('utf-8'))
			body.close()
			script.save()

			return HttpResponseRedirect(reverse('ups:project', args=[project_id]))

	context = {'project': project, 'form': form}
	return render(request, 'ups/create_script.html', context)
