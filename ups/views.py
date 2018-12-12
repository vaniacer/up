# -*- encoding: utf-8 -*-

from .forms import ServersFilterForm, ScriptsFilterForm, \
	HideInfoForm, UpdatesFilterForm, DumpsFilterForm, JobsFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, StreamingHttpResponse
from .permissions import check_perm_or404, check_permission
from django.contrib.auth.decorators import login_required
from .commands import run_cmd, info, commandick, back_url
from django.shortcuts import render, get_object_or_404
from .models import Project, Update, Script, History
from os.path import getsize, exists, join as opj
from django.conf import settings as conf
from wsgiref.util import FileWrapper
from re import search, IGNORECASE
from mimetypes import guess_type
from operator import itemgetter
from subprocess import call
from .dump import get_dumps
from os import remove


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
	check_perm_or404('dld_dump', current_project, request.user)
	return download(conf.MEDIA_ROOT + '/dumps/{project_name!s}/{file_name!s}'.format(
		project_name=current_project,
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
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)

	logids = data.getlist('logid')
	command = [opj(conf.BASE_DIR, '../env/bin/python'), 'killer.py']
	command.extend(logids)
	call(command)

	return HttpResponseRedirect(back_url(data))


@login_required
def mini_log(request):
	"""Выводит мини лог выполняющейся команды."""
	data = request.GET
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('run_command', current_project, request.user)

	logid = data.get('logid')
	event = get_object_or_404(History, uniq=logid)

	context = {
		'project': current_project,
		'panel':   'panel-default',
		'text':    'Working...',
		'cmd':     data['cmd'],
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
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('run_command', current_project, request.user)

	final = {}
	logids = data.getlist('logid')
	url = request.META['SERVER_NAME']
	qst = request.META['QUERY_STRING']
	context = {
		'name':    data['cmd'].capitalize().replace('_', ' '),
		'his':     commandick[data['cmd']].his,
		'cancel':  '/cancel/?%s' % qst,
		'project': current_project,
		'back':    back_url(data),
		'ok':      'btn-success',
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
				log = log.replace('<', '&lt;')
				log = log.replace('>', '&gt;')
				log = log.replace('__URL__', url)

		if exists(errfile):
			with open(errfile) as f:
				err = int(f.read())
			final[logid] = True

		context['logs'].extend([{'id': logid, 'log': log, 'err': err, 'event': event}])

	if all(value is True for value in final.values()):
		context['end'] = True

	return render(request, 'ups/command_log.html', context)


@login_required
def history(request, project_id):
	"""Выводит страницу истории."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('view_history',  current_project, request.user)

	hist = current_project.history_set.order_by('date').reverse()
	hist, hist_fd, hist_bk = pagination(request, hist)

	context = {
		'project': current_project,
		'hist_bk': hist_bk,
		'hist_fd': hist_fd,
		'history': hist,
	}

	return render(request, 'ups/history.html', context)


@login_required
def project(request, project_id):
	"""Выводит всю информацию о проекте, обрабатывает кнопки действий."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', current_project, request.user)

	data = request.GET

	if data.get('run_cmnd'):
		url = run_cmd(data, current_project, request.user)
		return HttpResponseRedirect(url)

	servers_filter = data.get('servers', '')
	servers = current_project.server_set.order_by('name')
	servers_filtered = servers.filter(name__iregex=servers_filter)
	servers_filter_form = ServersFilterForm(initial=data)

	scripts_filter = data.get('scripts', '')
	scripts = current_project.script_set.order_by('desc')
	scripts_filtered = scripts.filter(flnm__iregex=scripts_filter)
	scripts_filter_form = ScriptsFilterForm(initial=data)

	updates_filter = data.get('updates', '')
	updates = current_project.update_set.order_by('date').reverse()
	updates_filtered = updates.filter(flnm__iregex=updates_filter)
	updates_filter_form = UpdatesFilterForm(initial=data)

	dmplist_filter = data.get('dumps', '')
	dmplist = sorted(get_dumps(current_project.name) or '', key=itemgetter('date'), reverse=True)
	dmplist_filtered = [dump for dump in dmplist if search(dmplist_filter, dump['name'], IGNORECASE)]
	dmplist_filter_form = DumpsFilterForm(initial=data)

	hide_info_form = HideInfoForm(initial=data)

	context = {
		'info': info(data),
		'updates': updates,
		'dmplist': dmplist,
		'scripts': scripts,
		'servers': servers,
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

		commandsorted = sorted(commandick.itervalues(), key=lambda cmd: cmd.position)
		jobs = current_project.job_set.order_by('serv')
		jobs_filter = data.get('jobs', '')
		jobs_filtered = [
			job for job in jobs if search(jobs_filter, '{jobname!s} on {servername!s} {time!s}'.format(
				servername=job.serv,
				jobname=job,
				time=job.cdat,
			), IGNORECASE)
		]
		jobs_filter_form = JobsFilterForm(initial=data)

		logids = data.getlist('logid', default=[])
		cmdlog = data.get('cmdlog',  default=None)

		if len(logids) > 1:
			# Create allogs url if there are more then 1 log
			context['allogs'] = u'/command_log/?cmd={cmn_name!s}&prid={project_id!s}&logid={log_ids!s}'.format(
				log_ids='&logid='.join(logids),
				project_id=current_project.id,
				cmn_name=cmdlog,
			)

		context.update({
			'jobs_filter':   jobs_filter_form,
			'jobs_filtered': jobs_filtered,
			'commands': commandsorted,
			'cmdlog': cmdlog,
			'logs': logids,
			'jobs': jobs,
		})

	return render(request, 'ups/project.html', context)
