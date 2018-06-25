# -*- encoding: utf-8 -*-

from .forms import ServersFilterForm, ScriptsFilterForm, HideInfoForm, UpdatesFilterForm, DumpsFilterForm, JobsFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .permissions import check_perm_or404, check_permission
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .commands import run_cmd, info, commandick, back_url
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
	hist_fd = hist_pg[int(page):int(page) + 3]
	hist_bk = hist_pg[max(int(page) - 4, 0):int(page) - 1]
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
	Popen([conf.BASE_DIR + '/bash/killer.sh', ' '.join(logids)])

	return HttpResponseRedirect(back_url(data))


@login_required
def mini_log(request):
	"""Выводит страницу логов выполняющейся комманды."""
	data = request.GET
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('run_command', current_project, request.user)

	logid = data.get('logid')
	event = get_object_or_404(History, uniq=logid)

	context = {
		'project': current_project,
		'panel':   'panel-default',
		'text':    'Working ...',
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
	"""Выводит страницу логов выполняющейся комманды."""
	data = request.GET
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('run_command', current_project, request.user)

	tag = commandick[data['cmd']]['tag']
	qst = request.META['QUERY_STRING']
	url = request.META['SERVER_NAME']

	context = {
		'name':     data['cmd'].capitalize().replace('_', ' '),
		'cancel':  '/cancel/?%s' % qst,
		'project': current_project,
		'back':    back_url(data),
		'ok':      'btn-success',
		'tag':     tag,
		'logs':    [],
		'color':   '',
	}

	logids = data.getlist('logid')
	final = {}

	for logid in logids:

		final[logid] = False
		try:
			event = get_object_or_404(History, uniq=logid)
		except:
			event = None

		try:
			err = int(event.exit)
			final[logid] = True
			log = event.desc
			if err > 0:
				context['ok'] = 'btn-danger'
		except:
			try:
				log = open(conf.LOG_FILE + logid, 'r').read()
			except IOError:
				log = 'Working...'

			try:
				err = int(open(conf.ERR_FILE + logid, 'r').read())
				final[logid] = True
			except IOError:
				err = 999

		context['logs'].extend([{'id': logid, 'log': log.replace('__URL__', url), 'err': err, 'event': event}])

	if all(value is True for value in final.values()):
		context['end'] = True

	return render(request, 'ups/command_log.html', context)


@login_required
def history(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и скрипты, обрабатывает кнопки действий."""
	current_project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('run_command', current_project, request.user)

	history = current_project.history_set.order_by('date').reverse()
	history, hist_fd, hist_bk = pagination(request, history)

	context = {
		'project': current_project,
		'history': history,
		'hist_bk': hist_bk,
		'hist_fd': hist_fd,
	}

	return render(request, 'ups/history.html', context)


@login_required
def project(request, project_id):
	"""Выводит один проект, все его серверы, пакеты обновлений и скрипты, обрабатывает кнопки действий."""
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
	dmplist_filtered = [dump for dump in dmplist if re.search(dmplist_filter, dump['name'], re.IGNORECASE)]
	dmplist_filter_form = DumpsFilterForm(initial=data)

	commandsorted = sorted(commandick.itervalues(), key=itemgetter('position'))
	hide_info_form = HideInfoForm(initial=data)

	context = {
		'info': info(data),
		'updates': updates,
		'dmplist': dmplist,
		'scripts': scripts,
		'servers': servers,
		'commands': commandsorted,
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

		jobs_filter = data.get('jobs', '')
		jobs = current_project.job_set.order_by('serv')
		jobs_filtered = [
			job for job in jobs if re.search(jobs_filter, '{jobname!s} on {servername!s} {time!s}'.format(
				servername=job.serv,
				jobname=job,
				time=job.cdat,
			), re.IGNORECASE)
		]
		jobs_filter_form = JobsFilterForm(initial=data)

		get_cron_logs()

		logids = data.getlist('logid') or []
		cmdlog = data.get('cmdlog') or ''

		if len(logids) > 1:
			# Create allogs url if there are more then 1 log
			context['allogs'] = u'/command_log/?cmd={cmn_name!s}&prid={project_id!s}&logid={log_ids!s}'.format(
				log_ids='&logid='.join(logids),
				project_id=current_project.id,
				cmn_name=cmdlog,
			)

		context['jobs_filtered'] = jobs_filtered
		context['jobs_filter'] = jobs_filter_form
		context['cmdlog'] = cmdlog
		context['logs'] = logids
		context['jobs'] = jobs

	return render(request, 'ups/project.html', context)
