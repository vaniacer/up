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

	tag, his, job = command({'command': data['cmd']})

	logids = data.getlist('logid')

	for logid in logids:

		if his:
			history = get_object_or_404(History, uniq=logid)
			try:
				log = open(conf.LOG_FILE + logid, 'r').read()
			except IOError:
				log = ''

			text = '\n\n<%s{ Canceled :( }%s>' % ('-' * 46, '-' * 47)
			history.desc = log + text
			history.exit = 1
			history.save()

	opt = [conf.BASE_DIR + '/bash/killer.sh', ' '.join(logids)]
	Popen(opt)

	return HttpResponseRedirect('/projects/%s/?%s' % (data['prid'], info(data)))


@login_required
def command_log(request):
	"""Выводит страницу логов выполняющейся комманды."""
	data = request.GET
	current_project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project', current_project, request.user)
	check_perm_or404('run_command', current_project, request.user)

	tag, his, job = command({'command': data['cmd']})
	qst = request.META['QUERY_STRING']
	url = request.META['SERVER_NAME']

	context = {
		'back':    '/projects/%s/?%s' % (data['prid'], info(data)),
		'cancel':  '/cancel/?%s' % qst,
		'project': current_project,
		'ok':      'btn-success',
		'cmd':     data['cmd'],
		'tag':     tag,
		'logs':    [],
		'color':   '',
	}

	logids = data.getlist('logid')
	final = {}

	for logid in logids:

		final[logid] = False
		try:
			event = History.objects.get(uniq=logid)
		except:
			pass

		try:
			err = int(event.exit)
			final[logid] = True
			log = event.desc
			# pid = ''
			if err > 0:
				context['ok'] = 'btn-danger'
		except:
			try:
				log = open(conf.LOG_FILE + logid, 'r').read()
				# pid = open(conf.PID_FILE + logid, 'r').read()
			except IOError:
				log = 'Working...'
				# pid = ''

			try:
				err = int(open(conf.ERR_FILE + logid, 'r').read())
				final[logid] = True
			except IOError:
				err = 999

		context['logs'].extend([{'id': logid, 'log': log.replace('__URL__', url), 'err': err}])
		# context['cancel'] = context['cancel'] + '&pid=%s' % pid

	if all(value is True for value in final.values()):
		context['end'] = True

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
