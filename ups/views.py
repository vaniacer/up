# -*- encoding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Project, Update, Script
from django.conf import settings as conf
from .forms import SerfltrForm, HideForm
from .commands import command, cmd_run
from .commands_engine import add_event
from .commands_engine import add_job
from wsgiref.util import FileWrapper
from .permissions import check_perm
from .cron import get_cron_logs
from operator import itemgetter
from subprocess import Popen
from .dump import get_dumps
import mimetypes
import os
# from django.http import FileResponse


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


def delete_files(files):
	"""Удаляет список файлов."""
	for f in files:
		try:
			os.remove(f)
		except OSError:
			continue


def download(file_path, file_name):
	"""Скачать файл."""
	file_mimetype = mimetypes.guess_type(file_path)
	file_wrapper = FileWrapper(file(file_path, 'rb'))
	response = HttpResponse(file_wrapper, content_type=file_mimetype)
	response['Content-Disposition'] = 'attachment; filename=%s' % file_name
	response['Content-Length'] = os.stat(file_path).st_size
	response['X-Sendfile'] = file_path
	return response


@login_required
def download_upd(request, project_id, update_id):
	"""Скачать обновление."""
	update = get_object_or_404(Update, id=update_id)
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('dld_update', current_project, request.user)
	return download(str(update.file), str(update))


@login_required
def download_script(request, project_id, script_id):
	"""Скачать скрипт."""
	script = get_object_or_404(Script, id=script_id)
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('dld_script', current_project, request.user)
	return download(str(script.file), str(script))


@login_required
def download_dump(request, project_id, dump):
	"""Закачка дампов."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)
	return download(conf.MEDIA_ROOT + '/dumps/%s/%s' % (current_project.name, str(dump)), str(dump))


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


@login_required
def cancel(request, project_id, pid, cmd, log_id):
	"""Отмена команды."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)

	servers_filter = request.GET.get('servers', '')

	Popen(['kill', '-9', str(pid)])
	tag, his = command({'command': cmd, 'cron': '', })

	if his:
		log = open(conf.LOG_FILE + log_id, 'r').read()
		history = {'user': request.user, 'project': current_project, 'command': cmd}
		text = '\n\n<%s{ Canceled :( }%s>' % ('-' * 51, '-' * 52)
		add_event(history, log + text, 1, '', '')

	delete_files([conf.LOG_FILE + log_id, conf.PID_FILE + log_id, conf.ERR_FILE + log_id])

	return HttpResponseRedirect('/projects/%s/?servers=%s' % (project_id, servers_filter))


@login_required
def logs(request, project_id, log_id, cmd, rtype, date):
	"""Выводит лог выполняющейся комманды."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)

	data = request.GET

	tag, his = command({'command': cmd, 'cron': '', })
	log = open(conf.LOG_FILE + log_id, 'r').read()
	pid = open(conf.PID_FILE + log_id, 'r').read()
	url = request.META['SERVER_NAME']

	try:
		err = open(conf.ERR_FILE + log_id, 'r').read()
	except IOError:
		err = ''

	cdate = ''
	cron_id = ''
	date = date.replace('SS', ' ').replace('PP', ':').replace('OO', '-')

	history = {
		'date': date,
		'command': cmd,
		'user': request.user,
		'project': current_project,
	}

	context = {
		'log': log.replace('__URL__', url),
		'serfltr': data['servers'],
		'project': project_id,
		'log_id':  log_id,
		'tag': tag,
		'pid': pid,
		'cmd': cmd,
	}

	if err:
		context['err'] = int(err)
		if rtype == 'CRON':
			add_job(history, log, log_id)
			cdate, cron_id = date, log_id
			history['command'] = 'Set cron job - %s' % cmd.lower()
		if his:
			add_event(history, log, context['err'], cron_id, cdate)
		delete_files([conf.LOG_FILE + log_id, conf.PID_FILE + log_id, conf.ERR_FILE + log_id])

	return render(request, 'ups/output.html', context)
	# return FileResponse(open(conf.LOG_FILE + log_id, 'r'), content_type='text')


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и скрипты, обрабатывает кнопки действий."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm('view_project', current_project, request.user)

	data = request.GET
	get_cron_logs()

	servers_filter = data.get('servers', '')
	servers = current_project.server_set.order_by('name')
	srvfilt = servers.filter(name__iregex=servers_filter)
	serfltr = SerfltrForm(initial=data)
	hidefrm = HideForm(initial=data)

	dmplist = sorted(get_dumps(current_project.name) or '', key=itemgetter('date'), reverse=True)
	history = current_project.history_set.order_by('date').reverse()
	updates = current_project.update_set.order_by('date').reverse()
	cronjob = current_project.job_set.order_by('date').reverse()
	scripts = current_project.script_set.order_by('desc')

	history, hist_fd, hist_bk = pagination(request, history)

	context = {
		'project': current_project,
		'servers': servers,
		'srvfilt': srvfilt,
		'serfltr': serfltr,
		'updates': updates,
		'scripts': scripts,
		'cronjob': cronjob,
		'history': history,
		'hist_bk': hist_bk,
		'hist_fd': hist_fd,
		'dmplist': dmplist,
		'hidefrm': hidefrm, }

	if data.get('selected_command'):
		context = cmd_run(data, current_project, request.user, context)

	return render(request, 'ups/project.html', context)
