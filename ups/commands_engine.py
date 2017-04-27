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
	logs, errs = '', 0
	for i in selected['cronjbs']:
		try:
			Job.objects.get(cron=i).delete()
			log, err = run_cmd(['bash/delete_job.sh', '-job', i])
			logs += log
			errs += err
		except ObjectDoesNotExist:
			logs += 'Задача: %s не существует.\n' % str(i)
			continue

	add_event(selected, logs, errs, '', '')
	return logs, errs


def run_now(selected):
	"""Выполняет комманду."""
	opt = ['bash/' + selected['cmdname'], '-key', selected['key']]

	if selected['servers']:
		opt.extend(['-server', ' '.join(selected['servers'])])
	if selected['updates']:
		opt.extend(['-update', ' '.join(selected['updates'])])
	Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)


def run_now2(selected):
	"""Выполняет комманду."""
	opt = ['bash/' + selected['cmdname']]

	if selected['servers']:
		opt.extend(['-server', ' '.join(selected['servers'])])
	if selected['updates']:
		opt.extend(['-update', ' '.join(selected['updates'])])

	log, err = run_cmd(opt)
	if selected['history']:
		add_event(selected, log, err, '', '')
	return log, err


def cron_job(selected):
	"""Создает задачу в кроне."""
	key = get_key()
	opt = [
		conf.BASE_DIR + '/bash/cron_job.sh',
		'-date', selected['date'],
		'-cmd', selected['cmdname'],
		'-id', key, ]

	if selected['servers']:
		opt.extend(['-server', ' '.join(selected['servers'])])
	if selected['updates']:
		opt.extend(['-update', ' '.join(selected['updates'])])

	log, err = run_cmd(opt)
	add_job(selected, log, key)
	if selected['history']:
		selected['command'] = 'Set job - ' + selected['command']
		add_event(selected, log, err, key, '')
	return log, err
