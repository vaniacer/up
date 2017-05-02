# -*- encoding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as conf
from subprocess import Popen, PIPE
from .models import History, Job
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
		cron=cron,
		desc=log, )


def run_cmd(opt):
	"""Выполняет сценаий bash."""
	run = Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = run.communicate()
	rc = run.returncode
	return out + err, rc


def del_job(selected):
	for i in selected['cronjbs']:
		try:
			Job.objects.get(cron=i).delete()
		except ObjectDoesNotExist:
			# selected['log'] = 'Задача: %s не существует.\n' % str(i)
			continue


def starter(selected):
	"""Выполняет комманду."""
	opt = [conf.BASE_DIR + '/bash/starter.sh', '-cmd', selected['cmdname'], '-key', selected['key']]

	if selected['servers']:
		opt.extend(['-server', ' '.join(selected['servers'])])
	if selected['updates']:
		opt.extend(['-update', ' '.join(selected['updates'])])
	if selected['cronjbs']:
		opt.extend(['-job', ' '.join(selected['cronjbs'])])
		del_job(selected)
	if selected['cron']:
		opt.extend([
			'-run',  selected['cmdname'],
			'-date', selected['date'],
			'-key',  selected['key'],
			'-id',   selected['key'],
			'-cmd',  'cron.sh'])

	Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)
