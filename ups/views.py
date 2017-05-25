# -*- encoding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings as conf
from .commands import command, cmd_run
from .commands_engine import add_event
from .commands_engine import add_job
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from .permissions import check_perm
from .models import Project, Update
from .cron import get_cron_logs
import mimetypes
import os


def index(request):
	"""Домашняя страница приложения update server."""
	return render(request, 'ups/index.html')


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


def download(file_path, file_name):
	"""Закачка файлов."""
	file_mimetype = mimetypes.guess_type(file_path)
	file_wrapper = FileWrapper(file(file_path, 'rb'))
	response = HttpResponse(file_wrapper, content_type=file_mimetype)
	response['Content-Disposition'] = 'attachment; filename=%s' % file_name
	response['Content-Length'] = os.stat(file_path).st_size
	response['X-Sendfile'] = file_path
	return response


@login_required
def download_upd(request, project_id, update_id):
	"""Закачка обновлений."""
	update = get_object_or_404(Update, id=update_id)
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)
	return download(str(update.file), str(update))


@login_required
def download_dump(request, project_id, dump):
	"""Закачка дампов."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)
	return download(conf.MEDIA_ROOT + '/updates/dumps/' + str(dump), str(dump))


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


@login_required
def logs(request, project_id, log_id, cmd, cron, date):
	"""Выводит лог выполняющейся комманды."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)

	tag, his = command({'command': cmd, 'cron': '', })
	log = open(conf.LOG_FILE + log_id, 'r').read()
	try:
		err = open(conf.ERR_FILE + log_id, 'r').read()
	except IOError:
		err = ''

	context = {'log': log, 'tag': tag}
	history = {
		'date': date.replace('SS', ' ').replace('PP', ':').replace('OO', '.'),
		'user': request.user,
		'project': current_project,
		'command': cmd}

	if err:
		context['err'] = int(err)
		if cron == 'True':
			add_job(history, log, log_id)
			history['command'] = 'Set cron job - %s' % cmd.lower()
		if his:
			add_event(history, log, context['err'], '', '')
		os.remove(conf.LOG_FILE + log_id)
		os.remove(conf.ERR_FILE + log_id)
	return render(request, 'ups/output.html', context)


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
		context = cmd_run(request, current_project, context)
	return render(request, 'ups/project.html', context)
