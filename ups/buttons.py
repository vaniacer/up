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


def add_event(project, user, name, out, err, cron, date):
	History.objects.create(proj=project, user=user, name=name, desc=out, exit=err, cron=cron, cdat=date)


def run_cmd(opt):
	"""Выполняет комманду."""
	run = Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = run.communicate()
	rc = run.returncode

	return out + err, rc


def select_logs(selected):
	"""Обрабатывает событие select_logs."""

	servers = make_servers_lists(selected['servers'])

	opt = ['bash/logs.sh', servers]
	log, err = run_cmd(opt)

	return log, err


def select_ls(selected):
	"""Обрабатывает событие select_ls."""

	servers = make_servers_lists(selected['servers'])

	opt = ['bash/ls.sh', servers, ' ']
	log, err = run_cmd(opt)

	return log, err


def select_job_del(selected):

	jbs = '; '.join(selected['cronjbs'])
	opt = ['bash/cron_del.sh', jbs]
	log, err = run_cmd(opt)
	add_event(selected['project'], selected['user'], 'Delete cron job(s)', log, err, '', '')

	return log, err


def run_now(selected):
	"""Выполняет комманду."""

	updates = make_updates_lists(selected['updates'])
	servers = make_servers_lists(selected['servers'])

	opt = [
		'bash/' + selected['cmd'] + '.sh',
		'-server', servers,
		'-update', updates,
	]

	log, err = run_cmd(opt)
	add_event(selected['project'], selected['user'], 'Copy update(s) to server(s)', log, err, '', '')

	return log, err


def cron_job(selected):
	"""Создает задачу в кроне."""

	date, time = selected['date']

	updates = make_updates_lists(selected['updates'])
	servers = make_servers_lists(selected['servers'])

	key = b64encode(urandom(6), 'dfsDFAsfsf')
	opt = [
		conf.BASE_DIR + '/bash/cron_job.sh',
		'-server', servers,
		'-update', updates,
		'-date', date,
		'-time', time,
		'-cmd', selected['cmd'],
		'-id', str(key),
	]

	log, err = run_cmd(opt)
	add_event(selected['project'], selected['user'], 'Update server(s)', log, err, str(key), '')

	return log, err
