# -*- encoding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf
from django.http import FileResponse
from .permissions import check_perm
from .cron import get_cron_logs
from .commands import commands
from .models import Project
import datetime


def index(request):
	"""Домашняя страница приложения update server."""
	return render(request, 'ups/index.html')


def run_date():
	"""Если не указана дата, возвращает текущую дату + 1 минута."""
	date = datetime.datetime.now() + datetime.timedelta(minutes=1)
	return date.strftime("%d.%m.%Y %H:%M")


def cmd_render(request, current_project):
	"""Выводит результат нажатия кнопок."""
	check_perm('run_command', current_project, request.user)

	selected = {
		'user': request.user,
		'cron': request.POST.get('CRON') or '',
		'date': request.POST.get('selected_date') or run_date(),
		'updates': request.POST.getlist('selected_updates'),
		'servers': request.POST.getlist('selected_servers'),
		'cronjbs': request.POST.getlist('selected_jobs'),
		'command': request.POST.get('selected_commands'),
		'project': current_project, }

	context = {'project': current_project}
	cmd, url = commands(selected)
	cmd(selected)

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

	hist_pg = list(hist_pages.page_range)
	hist_fd = hist_pg[int(page):int(page) + 4]
	hist_bk = hist_pg[max(int(page) - 5, 0):int(page) - 1]
	return history, hist_fd, hist_bk


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


@login_required
def logs(request):
	"""Выводит логи."""
	log = FileResponse(open(conf.LOG_FILE, 'rb')).streaming_content
	err = open(conf.ERR_FILE, 'r').read()
	context = {'log': log}

	try:
		context['err'] = int(err)
	except ValueError:
		pass

	return render(request, 'ups/output_log.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и обрабатывает кнопки действий."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)

	get_cron_logs()
	servers = current_project.server_set.order_by('name')
	cronjob = current_project.job_set.order_by('date').reverse()
	updates = current_project.update_set.order_by('date').reverse()
	history = current_project.history_set.order_by('date').reverse()
	history, hist_fd, hist_bk = pagination(request, history)

	context = {
		'project': current_project,
		'servers': servers,
		'updates': updates,
		'cronjob': cronjob,
		'history': history,
		'hist_bk': hist_bk,
		'hist_fd': hist_fd, }

	if request.POST.get('selected_commands'):
		return cmd_render(request, current_project)

	return render(request, 'ups/project.html', context)
