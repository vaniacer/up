# -*- encoding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .cron import get_cron_jobs, get_cron_logs
from .permissions import check_perm
from .commands import commands
from .models import Project


def index(request):
	"""Домашняя страница приложения update server."""
	return render(request, 'ups/index.html')


def post_render(request, selected, cmd, url):
	"""Выводит результат нажатия кнопок."""
	check_perm('run_command', selected['project'], selected['user'])
	log, err = cmd(selected)
	context = {'project': selected['project'], 'log': log, 'err': err}
	if url:
		return HttpResponseRedirect(url)
	else:
		return render(request, 'ups/output.html', context)


def pagination(request, history):
	"""Создает страницы для закладки 'History'."""
	hist_pages = Paginator(history, 20)
	page = request.GET.get('page') or 1
	try:
		history = hist_pages.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		history = hist_pages.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		history = hist_pages.page(hist_pages.num_pages)

	hist_range = list(hist_pages.page_range)
	hist_fd = hist_range[int(page):int(page) + 4]
	back = max(int(page) - 5, 0)
	hist_bk = hist_range[back:int(page) - 1]
	return history, hist_fd, hist_bk


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и обрабатывает кнопки действий."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)

	get_cron_logs(current_project)
	cronjob = get_cron_jobs(current_project)
	servers = current_project.server_set.order_by('name')
	updates = current_project.update_set.order_by('date').reverse()
	history = current_project.history_set.order_by('date').reverse()
	history, hist_fd, hist_bk = pagination(request, history)

	selected = {
		'date': [
			request.POST.get('selected_date') or '__DATE__',
			request.POST.get('selected_time') or '__TIME__'],
		'cmd': ''.join([
			request.POST.get('select_copy') or '',
			request.POST.get('select_update') or '']),
		'updates': request.POST.getlist('selected_updates'),
		'servers': request.POST.getlist('selected_servers'),
		'cronjbs': request.POST.getlist('selected_jobs'),
		'project': current_project,
		'user': request.user,
	}

	context = {
		'project': current_project,
		'servers': servers,
		'updates': updates,
		'cronjob': cronjob,
		'history': history,
		'hist_bk': hist_bk,
		'hist_fd': hist_fd,
	}

	for key, value in commands.iteritems():
		if request.POST.get(key):
			return post_render(request, selected, value['cmd'], value['url'])

	return render(request, 'ups/project.html', context)
