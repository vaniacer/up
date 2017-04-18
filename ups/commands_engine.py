# -*- encoding: utf-8 -*-

from django.conf import settings as conf
from subprocess import Popen, PIPE
from .models import History, Job
from base64 import b64encode
from os import urandom


def add_event(selected, log, err, cron, date):
	"""Создает событие в истории."""
	History.objects.create(
		name=selected['command'].capitalize(),
		proj=selected['project'],
		user=selected['user'],
		cron=cron,
		cdat=date,
		desc=log,
		exit=err, )


def add_job(selected, log, cron):
	"""Создает запись о крон жобе."""
	Job.objects.create(
		name=selected['command'].capitalize(),
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
	opt = ['bash/delete_job.sh', '-job', ' '.join(selected['cronjbs'])]

	for i in selected['cronjbs']:
		try:
			Job.objects.get(cron=i).delete()
		except:
			continue

	log, err = run_cmd(opt)
	add_event(selected, log, err, '', '')
	return log, err


def run_now(selected):
	"""Выполняет комманду."""
	opt = ['bash/' + selected['command'] + '.sh']

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
	key = str(b64encode(urandom(6), 'dfsDFAsfsf'))
	opt = [
		conf.BASE_DIR + '/bash/cron_job.sh',
		'-date', selected['date'],
		'-cmd', selected['command'],
		'-id', key, ]

	if selected['servers']:
		opt.extend(['-server', ' '.join(selected['servers'])])
	if selected['updates']:
		opt.extend(['-update', ' '.join(selected['updates'])])

	log, err = run_cmd(opt)
	add_job(selected, log, key)
	return log, err
