# -*- encoding: utf-8 -*-

from .models import History, Job, Update, Script
from django.shortcuts import get_object_or_404
from django.conf import settings as conf
from subprocess import Popen
from base64 import b64encode
from os import urandom


def get_key():
	"""Создает случайную последовательность символов."""
	return str(b64encode(urandom(6), 'dfsDFAsfsf'))


def add_event(selected, log, err, cron, uniq, date, serv):
	"""Создает событие в истории."""
	History.objects.create(
		name=selected['name'].capitalize().replace('_', ' '),
		proj=selected['project'],
		user=selected['user'],
		serv=serv,
		cron=cron,
		uniq=uniq,
		cdat=date,
		desc=log,
		exit=err,
	)


def add_job(selected, log, cron, serv):
	"""Создает запись о крон жобе."""
	Job.objects.create(
		name=selected['command'].capitalize().replace('_', ' '),
		proj=selected['project'],
		user=selected['user'],
		cdat=selected['date'],
		perm=False,
		serv=serv,
		cron=cron,
		desc=log,
	)


def starter(selected):
	"""Выполняет комманду."""
	opt = [
		conf.BASE_DIR + '/bash/starter.sh',
		'-prj',  '%s:%s' % (str(selected['project'].id), str(selected['project'].name)),
		'-date', selected['date'],
		'-key',  selected['key']
	]

	opt.extend(selected['opt'])

	for ID in selected['updates']:
		update = get_object_or_404(Update, id=ID)
		opt.extend(['-u', str(update.file)])

	for ID in selected['scripts']:
		script = get_object_or_404(Script, id=ID)
		opt.extend(['-x', str(script.file)])

	for dump in selected['dumps']:
		opt.extend(['-m', str(dump)])

	if conf.DEBUG:
		print '\n', opt, '\n\n', selected, '\n'

	Popen(opt)
