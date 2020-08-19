# -*- encoding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, StreamingHttpResponse
from .permissions import check_permission, check_perm_or404
from django.contrib.auth.decorators import login_required
from .commands import run_cmd, info, commandick, back_url
from django.shortcuts import render, get_object_or_404
from .models import Project, Update, Script, History
from django.template.defaultfilters import register
from os.path import getsize, exists, join as opj
from re import sub, search, IGNORECASE, DOTALL
from django.conf import settings as conf
from wsgiref.util import FileWrapper
from commands import date_validate
from mimetypes import guess_type
from operator import itemgetter
from .forms import HideInfoForm
from django.http import Http404
from datetime import datetime
from subprocess import call
from .dump import get_dumps
from os import remove


@register.filter(name='target_blank', is_safe=True)
def url_target_blank(text):
	"""Добавляет target="_blank" к ссылкам автоматически созданным в описании сервера."""
	return text.replace('<a ', '<a target="_blank" ')


@register.filter(name='preview', is_safe=True)
def make_preview(text):
	"""Отрезает часть лога до 'результата'."""
	return sub(u'.*езультат:', '', text, flags=DOTALL)


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
	check_perm_or404('run_command',  project, request.user)

	logid = data.get('logid')
	event = get_object_or_404(History, uniq=logid)
	cname = event.name.lower().replace(' ', '_')
	check_perm_or404(commandick[cname].permission, project, request.user)

	context = {
		'panel': 'panel-default',
		'text':  'Working...',
		'event': event,
		'end':   False,
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
	project = get_object_or_404(Project, id=data['prid'])
	check_perm_or404('view_project',  project, request.user)
	check_perm_or404('run_command',   project, request.user)

	final = {}
	logids = data.getlist('logid')
	events = project.history_set.filter(uniq__in=logids)
	qst = request.META['QUERY_STRING']

	context = {
		'cancel': '/cancel/?%s' % qst,
		'back':   back_url(data),
		'ok':     'btn-success',
		'name':   'Command log',
		'logs':   [],
	}

	if len(logids) > 1:
		context['name'] = 'Multiple command log'

	for event in events:

		log = event.desc
		final[event.uniq] = False
		logfile = conf.LOG_FILE + event.uniq
		cname = event.name.replace('Set cron job - ', '').lower().replace(' ', '_')
		try:
			check_perm_or404(commandick[cname].permission, project, request.user)
		except KeyError:
			raise Http404

		if event.exit:
			final[event.uniq] = True

		if exists(logfile):
			with open(logfile) as f:
				log = f.read()

		context['logs'].extend([{'log': log, 'event': event}])

	if all(value is True for value in final.values()):
		context['end'] = True

	return render(request, 'ups/command_log.html', context)


@login_required
def history_view(request, project_id):
	"""Выводит страницу истории."""
	project = get_object_or_404(Project, id=project_id)
	check_perm_or404('view_project', project, request.user)
	check_perm_or404('view_history', project, request.user)

	furl = u''
	data = request.GET
	name = data.get('name', default='')
	serv = data.get('serv', default='')
	user = data.get('user', default='')
	dat1 = data.get('dat1', default='')
	dat2 = data.get('dat2', default='')
	servers = project.server_set.order_by('name')
	history = project.history_set.order_by('date').reverse()
	if dat1 and dat2:
		date_validate(dat1, '%Y\\-%m\\-%d')
		date_validate(dat2, '%Y\\-%m\\-%d')
		history = history.filter(date__range=[dat1, dat2])
		furl += u'&dat1={dat1}&dat2={dat2}'.format(dat1=dat1, dat2=dat2)
	elif dat1 and not dat2:
		furl += u'&dat1={}'.format(dat1)
		date_validate(dat1, '%Y\\-%m\\-%d')
		history = history.filter(date__date=dat1)
	if name:
		furl += u'&name={}'.format(name)
		history = history.filter(name__iregex=name)
	if serv:
		furl += u'&serv={}'.format(serv)
		history = history.filter(serv__name__iregex=serv)
	if user:
		furl += u'&user={}'.format(user)
		history = history.filter(user__username__iregex=user)

	hist, hifd, hibk = pagination(request, history)

	context = {
		'filter':  {'serv': serv, 'name': name, 'user': user, 'dat1': dat1, 'dat2': dat2, 'url': furl},
		'history': {'back': hibk, 'now': hist, 'forward': hifd},
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
		url = run_cmd(data, project, request)
		return HttpResponseRedirect(url)

	hide_details_form = HideInfoForm(initial=data)
	commandsorted = sorted(commandick.itervalues(), key=lambda cmd: cmd.position)

	history = project.history_set.order_by('date').reverse()
	history = history.filter(date__date=datetime.now(), user=request.user, cjob=False)
	running = history.filter(exit='').reverse()

	# -------------{filter servers}--------------
	srv_filter = data.get('servers', default=request.user.profile.server_fltr)
	if request.user.profile.server:
		# show only my servers
		servers = project.server_set.filter(user=request.user).order_by('name')
	else:
		servers = project.server_set.order_by('name')
	servers_filtered = servers.filter(name__iregex=srv_filter)

	# -------------{filter scripts}--------------
	scr_filter = data.get('scripts', default=request.user.profile.script_fltr)
	if request.user.profile.script:
		# show only my scripts
		scripts = project.script_set.filter(user=request.user).order_by('desc')
	else:
		scripts = project.script_set.order_by('desc')
	if not check_permission('run_sql_script', project, request.user):
		scripts = scripts.exclude(flnm__iregex='.sql')
	if not check_permission('run_script', project, request.user):
		scripts = scripts.exclude(flnm__iregex='.sh|.py|.yml')
	scripts_filtered = scripts.filter(flnm__iregex=scr_filter)

	# -------------{filter updates}--------------
	upd_filter = data.get('updates', default=request.user.profile.update_fltr)
	if request.user.profile.update:
		# show only my updates
		updates = project.update_set.filter(user=request.user).order_by('date').reverse()
	else:
		updates = project.update_set.order_by('date').reverse()
	updates_filtered = updates.filter(flnm__iregex=upd_filter)

	# -------------{filter dumps}----------------
	dmp_filter = data.get('dumps', default='')
	dmplist = sorted(get_dumps(project.name) or '', key=itemgetter('date'), reverse=True)
	dmplist_filtered = [dump for dump in dmplist if search(dmp_filter, dump['name'], IGNORECASE)]

	# -------------{filter jobs}-----------------
	job_filter = data.get('jobs', default=request.user.profile.cron_fltr)
	if request.user.profile.cron:
		# show only my jobs
		jobs = project.job_set.filter(user=request.user).order_by('serv')
	else:
		jobs = project.job_set.order_by('serv')
	jobs_filtered = [J for J in jobs if search(job_filter, '{name} on {serv} {date}'.format(
		name=J, serv=J.serv, date=J.cdat), IGNORECASE)]

	context = {
		'info':  info(data),
		'project':  project,
		'history':  history,
		'running':  running,
		'commands': commandsorted,
		'hide_info_form': hide_details_form,
		'jobs':    {'all': jobs,    'filtered': jobs_filtered},
		'updates': {'all': updates, 'filtered': updates_filtered},
		'dmplist': {'all': dmplist, 'filtered': dmplist_filtered},
		'scripts': {'all': scripts, 'filtered': scripts_filtered},
		'servers': {'all': servers, 'filtered': servers_filtered},
		'filter':  {'srv': srv_filter, 'scr': scr_filter, 'upd': upd_filter, 'dmp': dmp_filter, 'job': job_filter},
	}

	if len(running) > 1:
		# Create allogs url if there are more then 1 running log
		logids = '&logid='.join([i.uniq for i in running])
		context['allogs'] = u'/command_log/?&prid={pid!s}&logid={log!s}'.format(pid=project_id, log=logids)

	return render(request, 'ups/project.html', context)
