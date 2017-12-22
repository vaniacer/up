# -*- encoding: utf-8 -*-

from .models import History, Job, Server, Update, Script
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as conf
from subprocess import Popen
from base64 import b64encode
from os import urandom


def get_key():
	"""Создает случайную последовательность символов."""
	return str(b64encode(urandom(6), 'dfsDFAsfsf'))


def add_event(selected, log, err, cron, date):
	"""Создает событие в истории."""
	History.objects.create(
		name=selected['command'].capitalize().replace('_', ' '),
		proj=selected['project'],
		user=selected['user'],
		cron=cron,
		cdat=date,
		desc=log,
		exit=err, )


def add_job(selected, log, cron):
	"""Создает запись о крон жобе."""
	Job.objects.create(
		name=selected['command'].capitalize().replace('_', ' '),
		proj=selected['project'],
		user=selected['user'],
		cdat=selected['date'],
		perm=False,
		cron=cron,
		desc=log, )


def del_job(job):
	"""Удаляет из базы запись о крон жобе."""
	try:
		Job.objects.get(cron=job).delete()
	except ObjectDoesNotExist:
		pass


def job_opt(selected, cron):
	"""В зависимости от выбранного действия с кронжобом, удаляет либо меняет job.perm статус."""
	try:
		job = Job.objects.get(cron=cron)
		if selected['command'] == 'cancel_job':
			job.delete()
		if selected['command'] == 'permanent_job':
			job.perm = True
			job.save()
		if selected['command'] == 'once_job':
			job.perm = False
			job.save()

	except ObjectDoesNotExist:
		pass


def starter(selected):
	"""Выполняет комманду."""
	opt = [conf.BASE_DIR + '/bash/starter.sh']

	if selected['rtype'] == 'CRON':
		opt.extend([
			'-run',  selected['cmdname'],
			'-date', selected['date'],
			'-cmd',  'cron.sh'])
	else:
		opt.extend(['-cmd', selected['cmdname']])

	opt.extend([
		'-prj', '%s:%s' % (str(selected['project'].id), str(selected['project'].name)),
		'-key', selected['key']])

	for ID in selected['servers']:
		server = Server.objects.get(id=ID)
		opt.extend(['-s', '%s:%s:%s' % (server.addr, server.wdir, server.port)])

	for ID in selected['updates']:
		update = Update.objects.get(id=ID)
		opt.extend(['-u', str(update.file)])

	for ID in selected['scripts']:
		script = Script.objects.get(id=ID)
		opt.extend(['-x', str(script.file)])

	for dump in selected['dumps']:
		opt.extend(['-m', str(dump)])

	for cronjb in selected['cronjbs']:
		opt.extend(['-j', str(cronjb)])
		job_opt(selected, cronjb)

	if conf.DEBUG:
		print '\n', opt, '\n\n', selected, '\n'
	Popen(opt)
