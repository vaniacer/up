# -*- encoding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ServersFilterForm, ScriptsFilterForm, HideInfoForm
from .forms import UpdatesFilterForm, DumpsFilterForm, JobsFilterForm
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .commands import run_cmd, info, commandick, back_url
from django.shortcuts import render, get_object_or_404
from .models import Project, Update, Script, History
from django.template.defaultfilters import register
from os.path import getsize, exists, join as opj
from .permissions import check_perm_or404
from django.conf import settings as conf
from wsgiref.util import FileWrapper
from commands import date_validate
from re import search, IGNORECASE
from mimetypes import guess_type
from operator import itemgetter
from subprocess import call
from .dump import get_dumps
from os import remove
from datetime import datetime


@register.filter(name='target_blank', is_safe=True)
def url_target_blank(text):
	"""Добавляет target="_blank" к ссылкам автоматически созданным в описании сервера."""
	return text.replace('<a ', '<a target="_blank" ')


def index(request):
	"""Домашняя страница приложения update server."""
	return render(request, 'ups/index.html')


def pagination(request, hist):
	"""Создает страницы для History."""
	hist_pages = Paginator(hist, 20)
	page = request.GET.get('page') or 1
	try:
		hist = hist_pages.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		hist = hist_pages.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		hist = hist_pages.page(hist_pages.num_pages)

	hist_pg = list(hist_pages.page_range)
	hist_fd = hist_pg[int(page):int(page) + 3]
	hist_bk = hist_pg[max(int(page) - 4, 0):int(page) - 1]
	return hist, hist_fd, hist_bk


def delete_files(files):
	"""Удаляет список файлов."""
	for f in files:
		if exists(f):
			remove(f)


def download(file_path, file_name):
	"""Потоковая качалка"""
	file_wrap = FileWrapper(open(file_path, 'rb'), blksize=8192)
	file_type = guess_type(file_path)
	file_size = getsize(file_path)

	response = StreamingHttpResponse(file_wrap, content_type=file_type)
	response['Content-Disposition'] = "attachment; filename=%s" % file_name
	response['Content-Length'] = file_size
	return response


@login_required
def download_upd(request, project_id, update_id):
	"""Скачать обновление."""
	update = get_object_or_404(Update,   id=update_id)
	project = get_object_or_404(Project, id=project_id)
	check_perm_or404('dld_update', project, request.user)
	return download(str(update.file), str(update))


@login_required
def download_script(request, project_id, script_id):
	"""Скачать скрипт."""
	script = get_object_or_404(Script,   id=script_id)
	project = get_object_or_404(Project, id=project_id)
	check_perm_or404('dld_script', project, request.user)
	return download(str(script.file), str(script))


@login_required
def download_dump(request, project_id, dump):
	"""Закачка дампов."""
	project = get_object_or_404(Project, id=project_id)
	check_perm_or404('dld_dump', project, request.user)
	return download(conf.MEDIA_ROOT + '/dumps/{project_name!s}/{file_name!s}'.format(
		project_name=project,
		file_name=dump
	), str(dump))


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
	project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('run_command', project, request.user)

	logids = data.getlist('logid')
	context = {'info': info(data), 'project': project}
	command = [opj(conf.BASE_DIR, '../env/bin/python'), 'killer.py']
	command.extend(logids)
	call(command)

	return render(request, 'ups/cancel.html', context)


@login_required
def mini_log(request):
	"""Выводит мини лог выполняющейся команды."""
	data = request.GET
	project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', project, request.user)
	check_perm_or404('run_command', project, request.user)

	logid = data.get('logid')
	event = get_object_or_404(History, uniq=logid)

	context = {
		'panel':   'panel-default',
		'text':    'Working...',
		'cmd':     event.name,
		'project': project,
		'event':   event,
		'end':     False,
	}

	if event.exit:
		context['end'] = True
		if int(event.exit) > 0:
			context['panel'] = 'panel-danger'
			context['text'] = 'Done :('
		else:
			context['panel'] = 'panel-success'
			context['text'] = 'Done :)'

	return render(request, 'ups/command_log_mini.html', context)


@login_required
def command_log(request):
	"""Выводит страницу логов выполняющейся команды."""
	data = request.GET
	cname = data['cmd'].lower().replace(' ', '_')
	project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404(commandick[cname].permission,  project, request.user)

	final = {}
	logids = data.getlist('logid')
	url = request.META['SERVER_NAME']
	qst = request.META['QUERY_STRING']
	context = {
		'his':     commandick[cname].his,
		'cancel':  '/cancel/?%s' % qst,
		'back':    back_url(data),
		'ok':      'btn-success',
		'name':    data['cmd'],
		'project': project,
		'logs':    [],
		'color':   '',
	}

	for logid in logids:

		err = 999
		event = None
		log = 'Working...'
		final[logid] = False
		logfile = conf.LOG_FILE + logid
		errfile = conf.ERR_FILE + logid

		if context['his']:
			event = get_object_or_404(History, uniq=logid)
			log = event.desc
			if event.exit:
				err = int(event.exit)
				final[logid] = True

		if exists(logfile):
			with open(logfile) as f:
				log = f.read()

		if exists(errfile):
			with open(errfile) as f:
				err = int(f.read())
			final[logid] = True

		context['logs'].extend([{'id': logid, 'log': log.replace('__URL__', url), 'err': err, 'event': event}])

	if all(value is True for value in final.values()):
		context['end'] = True

	return render(request, 'ups/command_log.html', context)


@login_required
def history_view(request, project_id):
	"""Выводит страницу истории."""
	project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', project, request.user)
	check_perm_or404('view_history', project, request.user)

	data = request.GET
	name = data.get('name', default='')
	date = data.get('date', default='')
	servers = project.server_set.order_by('name')
	history = project.history_set.order_by('date').reverse()
	if name:
		history = history.filter(serv__name__iregex=name)
	if date:
		date_validate(date, '%Y\\-%m\\-%d')
		history = history.filter(date__date=date)
	hist, hifd, hibk = pagination(request, history)

	context = {
		'history': {'back': hibk, 'now':  hist, 'forward': hifd},
		'filter':  {'name': name, 'date': date},
		'project': project,
		'servers': servers,
	}

	return render(request, 'ups/history.html', context)


@login_required
def project_view(request, project_id):
	"""Выводит всю информацию о проекте, обрабатывает кнопки действий."""
	project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', project, request.user)

	data = request.GET
	if data.get('run_cmnd'):
		url = run_cmd(data, project, request.user)
		return HttpResponseRedirect(url)

	logids = data.getlist('logid', default=[])
	cmdlog = data.get('cmdlog',  default=None)

	hide_details_form = HideInfoForm(initial=data)
	commandsorted = sorted(commandick.itervalues(), key=lambda cmd: cmd.position)

	today = datetime.now()
	history = project.history_set.order_by('date').reverse()
	history = history.filter(date__date=today, user=request.user)
	running = history.filter(exit='')

	servers_filter = data.get('servers', default='')
	servers = project.server_set.order_by('name')
	servers_filtered = servers.filter(name__iregex=servers_filter)
	servers_filter_form = ServersFilterForm(initial=data)

	scripts_filter = data.get('scripts', default='')
	scripts = project.script_set.order_by('desc')
	scripts_filtered = scripts.filter(flnm__iregex=scripts_filter)
	scripts_filter_form = ScriptsFilterForm(initial=data)

	updates_filter = data.get('updates', default='')
	updates = project.update_set.order_by('date').reverse()
	updates_filtered = updates.filter(flnm__iregex=updates_filter)
	updates_filter_form = UpdatesFilterForm(initial=data)

	dmplist_filter = data.get('dumps', default='')
	dmplist = sorted(get_dumps(project.name) or '', key=itemgetter('date'), reverse=True)
	dmplist_filtered = [dump for dump in dmplist if search(dmplist_filter, dump['name'], IGNORECASE)]
	dmplist_filter_form = DumpsFilterForm(initial=data)

	jobs = project.job_set.order_by('serv')
	jobs_filter = data.get('jobs', default='')
	jobs_filtered = [J for J in jobs if search(jobs_filter, '{name} on {serv} {date}'.format(
		name=J, serv=J.serv, date=J.cdat), IGNORECASE)]
	jobs_filter_form = JobsFilterForm(initial=data)

	context = {
		'jobs': jobs,
		'logs': logids,
		'info': info(data),

		'cmdlog':   cmdlog,
		'project':  project,
		'updates':  updates,
		'dmplist':  dmplist,
		'scripts':  scripts,
		'servers':  servers,
		'history':  history,
		'running':  running,
		'commands': commandsorted,

		'jobs_filtered':    jobs_filtered,
		'servers_filtered': servers_filtered,
		'scripts_filtered': scripts_filtered,
		'updates_filtered': updates_filtered,
		'dmplist_filtered': dmplist_filtered,

		'jobs_filter':    jobs_filter_form,
		'hide_info_form': hide_details_form,
		'servers_filter': servers_filter_form,
		'scripts_filter': scripts_filter_form,
		'updates_filter': updates_filter_form,
		'dmplist_filter': dmplist_filter_form,
	}

	if len(running) > 1:
		# Create allogs url if there are more then 1 running log
		running_list = list(running)
		logids = [i.uniq for i in running_list]
		context['allogs'] = u'/command_log/?cmd={cmd!s}&prid={pid!s}&logid={log!s}'.format(
			cmd=cmdlog, pid=project_id, log='&logid='.join(logids))

	return render(request, 'ups/project.html', context)
