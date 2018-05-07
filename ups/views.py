# -*- encoding: utf-8 -*-

from .forms import ServersFilterForm, ScriptsFilterForm, HideInfoForm, UpdatesFilterForm, DumpsFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .permissions import check_perm_or404, check_permission
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .commands import command, cmd_run, info, commandick
from django.shortcuts import render, get_object_or_404
from .models import Project, Update, Script, History
from django.conf import settings as conf
from wsgiref.util import FileWrapper
from .cron import get_cron_logs
from operator import itemgetter
from subprocess import Popen
from .dump import get_dumps
import mimetypes
import os
import re


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
	check_perm_or404('dld_update', current_project, request.user)
	return download(str(update.file), str(update))


@login_required
def download_script(request, project_id, script_id):
	"""Скачать скрипт."""
	script = get_object_or_404(Script, id=script_id)
	current_project = get_object_or_404(Project, id=project_id)
	check_perm_or404('dld_script', current_project, request.user)
	return download(str(script.file), str(script))


@login_required
def download_dump(request, project_id, dump):
	"""Закачка дампов."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', current_project, request.user)
	return download(conf.MEDIA_ROOT + '/dumps/%s/%s' % (current_project.name, str(dump)), str(dump))


@login_required
def projects(request):
	"""Выводит список проектов."""
	project_list = Project.objects.order_by('name')
	context = {'projects': project_list}
	return render(request, 'ups/projects.html', context)


@login_required
def cancel(request):
	"""Отмена выполняющейся команды."""
	data = request.GET
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)

	Popen(['kill', '-9', data['pid']])
	tag, his = command({'command': data['cmd']})

	if his:
		history = get_object_or_404(History, id=data['hid'])
		log = open(conf.LOG_FILE + data['logid'], 'r').read()
		text = '\n\n<%s{ Canceled :( }%s>' % ('-' * 51, '-' * 52)
		history.desc = log + text
		history.exit = 1
		history.save()

	delete_files([conf.LOG_FILE + data['logid'], conf.PID_FILE + data['logid'], conf.ERR_FILE + data['logid']])

	return HttpResponseRedirect('/projects/%s/?%s' % (data['prid'], info(data)))


@login_required
def command_log(request):
	"""Выводит страницу логов выполняющейся комманды."""
	data = request.GET
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('run_command', current_project, request.user)

	tag, his = command({'command': data['cmd']})
	qst = request.META['QUERY_STRING']
	url = request.META['SERVER_NAME']

	try:
		log = open(conf.LOG_FILE + data['logid'], 'r').read()
		pid = open(conf.PID_FILE + data['logid'], 'r').read()
	except IOError:
		return HttpResponseRedirect('/projects/%s/?%s' % (data['prid'], info(data)))

	try:
		err = open(conf.ERR_FILE + data['logid'], 'r').read()
	except IOError:
		err = ''

	context = {
		'back':    '/projects/%s/?%s' % (data['prid'], info(data)),
		'cancel':  '/cancel/?pid=%s&%s' % (pid, qst),
		'log':     log.replace('__URL__', url),
		'project': current_project,
		'ok':      'btn-success',
		'log_id':  data['logid'],
		'rtype':   data['rtype'],
		'key':     data['logid'],
		'cmd':     data['cmd'],
		'tag':     tag,
		'pid':     pid,
		'color':   '',
	}

	if err:
		context['err'] = int(err)
		if context['err'] > 0:
			context['color'] = '#f2dede'
			context['ok'] = 'btn-danger'

	return render(request, 'ups/command_log.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и скрипты, обрабатывает кнопки действий."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', current_project, request.user)

	data = request.GET
	get_cron_logs()

	servers_filter = data.get('servers', '')
	servers = current_project.server_set.order_by('name')
	servers_filtered = servers.filter(name__iregex=servers_filter)
	servers_filter_form = ServersFilterForm(initial=data)

	scripts_filter = data.get('scripts', '')
	scripts = current_project.script_set.order_by('desc')
	scripts_filtered = scripts.filter(file__iregex=scripts_filter)
	scripts_filter_form = ScriptsFilterForm(initial=data)

	updates_filter = data.get('updates', '')
	updates = current_project.update_set.order_by('date').reverse()
	updates_filtered = updates.filter(file__iregex=updates_filter)
	updates_filter_form = UpdatesFilterForm(initial=data)

	dmplist_filter = data.get('dumps', '')
	dmplist = sorted(get_dumps(current_project.name) or '', key=itemgetter('date'), reverse=True)
	dmplist_filtered = [dump for dump in dmplist if re.search(dmplist_filter, dump['name'], re.IGNORECASE)]
	dmplist_filter_form = DumpsFilterForm(initial=data)

	commanddlist = sorted(commandick.itervalues(), key=itemgetter('menu'))
	hide_info_form = HideInfoForm(initial=data)

	context = {
		'info': info(data),
		'updates': updates,
		'dmplist': dmplist,
		'scripts': scripts,
		'servers': servers,
		'commands': commanddlist,
		'project': current_project,
		'hide_info_form': hide_info_form,
		'servers_filtered': servers_filtered,
		'servers_filter': servers_filter_form,
		'scripts_filtered': scripts_filtered,
		'scripts_filter': scripts_filter_form,
		'updates_filtered': updates_filtered,
		'updates_filter': updates_filter_form,
		'dmplist_filtered': dmplist_filtered,
		'dmplist_filter': dmplist_filter_form,
	}

	if check_permission('run_command', current_project, request.user):
		history = current_project.history_set.order_by('date').reverse()
		cronjob = current_project.job_set.order_by('date').reverse()
		history, hist_fd, hist_bk = pagination(request, history)
		context['cronjob'] = cronjob
		context['history'] = history
		context['hist_bk'] = hist_bk
		context['hist_fd'] = hist_fd

		if data.get('selected_command'):
			url = cmd_run(data, current_project, request.user)
			return HttpResponseRedirect(url)

	return render(request, 'ups/project.html', context)
