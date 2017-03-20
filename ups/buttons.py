# -*- encoding: utf-8 -*-

from .models import Server, Update, History
from subprocess import Popen, PIPE


def make_lists(selected_updates, selected_servers):
	"""Создает списки избранных серверов и апдейтов."""

	updates = []
	servers = []

	for i in selected_updates:
		updates.append(Update.objects.get(id=i))

	for i in selected_servers:
		servers.append(Server.objects.get(id=i))

	# print updates, '\n', servers
	return [servers, updates]


def run_cmd(opt):
	run = Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = run.communicate()
	rc = run.returncode
	return out + err, rc


def add_event(project, name, out, err):
	History.objects.create(proj=project, name=name, desc=out, exit=err)


def select_test(selected_updates, selected_servers, project):
	"""Обрабатывает событие select_test."""

	selected = make_lists(selected_updates, selected_servers)
	servers = selected[0]
	updates = selected[1]

	obj = ' '.join(str(u) for u in updates) + ' ' + ' '.join(str(s.addr) for s in servers)
	opt = ['bash/test', obj]

	log, err = run_cmd(opt)
	add_event(project, 'Test', log, err)
	return log, err


def select_upload(selected_updates, selected_servers, project):
	"""Обрабатывает событие select_upload."""

	selected = make_lists(selected_updates, selected_servers)
	servers = selected[0]
	updates = selected[1]

	srv = ' '.join(str(s.addr) + ':' + str(s.wdir) for s in servers)
	upd = ' '.join('media/' + str(u.file) for u in updates)
	opt = ['bash/copy.sh', '-server', srv, '-update', upd]

	log, err = run_cmd(opt)
	add_event(project, 'Upload to servers', log, err)

	return log, err
