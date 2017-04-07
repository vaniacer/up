# -*- encoding: utf-8 -*-

from .models import Server, Update, History
from django.conf import settings as conf
from subprocess import Popen, PIPE
from base64 import b64encode
from os import urandom


def make_updates_lists(selected_updates):
	"""Создает списки избранных апдейтов."""

	updates = []

	for i in selected_updates:
		updates.append(Update.objects.get(id=i))

	upd = ' '.join(conf.MEDIA_ROOT + '/' + str(u.file) for u in updates)

	return upd


def make_servers_lists(selected_servers):
	"""Создает списки избранных серверов."""

	servers = []

	for i in selected_servers:
		servers.append(Server.objects.get(id=i))

	srv = ' '.join(str(s.addr) + ':' + str(s.wdir) for s in servers)

	return srv


def run_cmd(opt):
	"""Выполняет комманду."""
	run = Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = run.communicate()
	rc = run.returncode

	return out + err, rc


def add_event(project, user, name, out, err, cron, date):
	History.objects.create(proj=project, user=user, name=name, desc=out, exit=err, cron=cron, cdat=date)


def select_copy(selected_updates, selected_servers, project, user):
	"""Обрабатывает событие select_copy."""

	servers = make_servers_lists(selected_servers)
	updates = make_updates_lists(selected_updates)

	opt = ['bash/copy.sh', '-server', servers, '-update', updates]

	log, err = run_cmd(opt)
	add_event(project, user, 'Copy update(s) to server(s)', log, err, '', '')

	return log, err


def select_cron_copy(selected_updates, selected_servers, project, user, date, time):
	"""Обрабатывает событие select_copy."""

	if not date:
		date = '__DATE__'

	if not time:
		time = '__TIME__'

	servers = make_servers_lists(selected_servers)
	updates = make_updates_lists(selected_updates)

	key = b64encode(urandom(6), 'dfsDFAsfsf')
	opt = [
		conf.BASE_DIR + '/bash/cron_copy.sh',
		'-server', servers,
		'-update', updates,
		'-date', date,
		'-time', time,
		'-id', str(key)
	]

	log, err = run_cmd(opt)
	add_event(project, user, 'Set cron job - Copy update(s) to server(s)', log, err, str(key), '')

	return log, err


def select_logs(selected_servers):
	"""Обрабатывает событие select_logs."""

	servers = make_servers_lists(selected_servers)

	opt = ['bash/logs.sh', servers]
	log, err = run_cmd(opt)

	return log, err


def select_ls(selected_servers):
	"""Обрабатывает событие select_ls."""

	servers = make_servers_lists(selected_servers)

	opt = ['bash/ls.sh', servers, ' ']
	log, err = run_cmd(opt)

	return log, err


def select_job_del(selected_jobs, project, user):

	jbs = '; '.join(selected_jobs)
	print jbs
	opt = ['bash/cron_del.sh', jbs]
	log, err = run_cmd(opt)
	add_event(project, user, 'Delete cron job(s)', log, err, '', '')

	return log, err
