# -*- encoding: utf-8 -*-

from .models import Server, Update, History
from subprocess import Popen, PIPE


def make_updates_lists(selected_updates):
	"""Создает списки избранных апдейтов."""

	updates = []

	for i in selected_updates:
		updates.append(Update.objects.get(id=i))

	return updates


def make_servers_lists(selected_servers):
	"""Создает списки избранных серверов."""

	servers = []

	for i in selected_servers:
		servers.append(Server.objects.get(id=i))

	return servers


def run_cmd(opt):
	"""Выполняет комманду."""
	run = Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = run.communicate()
	rc = run.returncode

	return out + err, rc


def add_event(project, name, out, err):
	History.objects.create(proj=project, name=name, desc=out, exit=err)


def select_test(selected_updates, selected_servers, project):
	"""Обрабатывает событие select_test."""

	servers = make_servers_lists(selected_servers)
	updates = make_updates_lists(selected_updates)

	obj = ' '.join(str(u) for u in updates) + ' ' + ' '.join(str(s.addr) for s in servers)
	opt = ['bash/test', obj]

	log, err = run_cmd(opt)
	add_event(project, 'Test', log, err)

	return log, err


def select_copy(selected_updates, selected_servers, project):
	"""Обрабатывает событие select_copy."""

	servers = make_servers_lists(selected_servers)
	updates = make_updates_lists(selected_updates)

	srv = ' '.join(str(s.addr) + ':' + str(s.wdir) for s in servers)
	upd = ' '.join('media/' + str(u.file) for u in updates)
	opt = ['bash/copy.sh', '-server', srv, '-update', upd]

	log, err = run_cmd(opt)
	add_event(project, 'Copy update(s) to server(s)', log, err)

	return log, err


def select_cron_copy(selected_updates, selected_servers, project, date, time):
	"""Обрабатывает событие select_copy."""

	servers = make_servers_lists(selected_servers)
	updates = make_updates_lists(selected_updates)

	srv = ' '.join(str(s.addr) + ':' + str(s.wdir) for s in servers)
	upd = ' '.join('media/' + str(u.file) for u in updates)
	opt = ['bash/cron_copy.sh', '-server', srv, '-update', upd, '-date', date, '-time', time]

	log, err = run_cmd(opt)
	add_event(project, 'Set cron job - Copy update(s) to server(s)', log, err)

	return log, err


def select_logs(selected_servers):
	"""Обрабатывает событие select_logs."""

	servers = make_servers_lists(selected_servers)

	srv = ' '.join(str(s.addr) + ':' + str(s.wdir) for s in servers)
	opt = ['bash/logs.sh', srv]
	log, err = run_cmd(opt)

	return log, err

def select_ls(selected_servers):
	"""Обрабатывает событие select_ls."""

	servers = make_servers_lists(selected_servers)

	srv = ' '.join(str(s.addr) + ':' + str(s.wdir) for s in servers)
	opt = ['bash/ls.sh', srv]
	log, err = run_cmd(opt)

	return log, err


def select_job_del(selected_jobs, project):

	jbs = '; '.join(selected_jobs)
	opt = ['bash/cron_del.sh', jbs]
	log, err = run_cmd(opt)
	add_event(project, 'Delete cron job(s)', log, err)

	return log, err
