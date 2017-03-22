# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from .buttons import select_test, select_copy, select_cron_copy, select_logs
from .models import Project
from django.shortcuts import render
from .permissions import check_perm


def get_cron_jobs(current_project):
	"""Получает список заданий в кроне для проекта."""

	pass


def index(request):
	"""Домашняя страница приложения update server"""
	return render(request, 'ups/index.html')


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и обрабатывает кнопки действий."""
	current_project = Project.objects.get(id=project_id)

	check_perm('view_project', current_project, request.user)

	servers = current_project.server_set.order_by('name')
	updates = current_project.update_set.order_by('date').reverse()
	history = current_project.history_set.order_by('date').reverse()
	cronjob = get_cron_jobs(current_project)

	selected_updates = request.POST.getlist('selected_updates')
	selected_servers = request.POST.getlist('selected_servers')

	date = request.POST.get('selected_date')
	time = request.POST.get('selected_time')

	# print selected_date, selected_time

	if request.POST.get('select_test'):
		print request.POST
		check_perm('run_command', current_project, request.user)
		log, err = select_test(selected_updates, selected_servers, current_project)
		context = {'project': current_project, 'log': log, 'err': err}
		return render(request, 'ups/output.html', context)

	if request.POST.get('select_copy'):
		check_perm('run_command', current_project, request.user)
		if date and time:
			log, err = select_cron_copy(selected_updates, selected_servers, current_project, date, time)
		else:
			log, err = select_copy(selected_updates, selected_servers, current_project)
		context = {'project': current_project, 'log': log, 'err': err}
		return render(request, 'ups/output.html', context)

	if request.POST.get('select_logs'):
		check_perm('run_command', current_project, request.user)
		log, err = select_logs(selected_servers)
		context = {'project': current_project, 'log': log, 'err': err}
		return render(request, 'ups/output.html', context)

	context = {
		'project': current_project,
		'servers': servers,
		'updates': updates,
		'history': history,
		'cronjob': cronjob,
	}

	return render(request, 'ups/project.html', context)
