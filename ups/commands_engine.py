# -*- encoding: utf-8 -*-

from django.conf import settings as conf
from subprocess import Popen, PIPE
from .models import History, Job
from base64 import b64encode
from os import urandom
import datetime


def add_event(selected, log, err, cron, date):
	"""Создает событие в истории."""
	History.objects.create(
		name=selected['cmd'].capitalize(),
		proj=selected['project'],
		user=selected['user'],
		cron=cron,
		cdat=date,
		desc=log,
		exit=err, )


def add_job(selected, log, cron, kill):
	"""Создает запись о крон жобе."""
	date = selected['date']
	if date == '__DATE__':
		date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

	Job.objects.create(
		name=selected['cmd'].capitalize(),
		proj=selected['project'],
		user=selected['user'],
		cdat=date,
		kill=kill,
		cron=cron,
		desc=log, )


def del_job(selected):
	for i in selected['cronjbs']:
		Job.objects.get(cron=i).delete()


def run_cmd(opt):
	"""Выполняет сценаий bash."""
	run = Popen(opt, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = run.communicate()
	rc = run.returncode
	return out + err, rc


def select_logs(selected):
	"""Обрабатывает событие select_logs."""
	opt = ['bash/logs.sh', ' '.join(selected['servers'])]
	log, err = run_cmd(opt)
	return log, err


def select_ls(selected):
	"""Обрабатывает событие select_ls."""
	opt = ['bash/ls.sh', ' '.join(selected['servers']), ' ']
	log, err = run_cmd(opt)
	return log, err


def select_job_del(selected):
	"""Обрабатывает событие select_job_del."""
	jbs = '; '.join(Job.objects.get(cron=i).kill for i in selected['cronjbs'])
	opt = ['bash/cron_del.sh', jbs]
	log, err = run_cmd(opt)
	selected['cmd'] = 'Delete cron job(s)'
	add_event(selected, log, err, '-/-', '')
	del_job(selected)
	return log, err


def run_now(selected):
	"""Выполняет комманду."""
	opt = [
		'bash/' + selected['cmd'] + '.sh',
		'-server', ' '.join(selected['servers']),
		'-update', ' '.join(selected['updates']), ]

	log, err = run_cmd(opt)
	add_event(selected, log, err, '', '')
	return log, err


def cron_job(selected):
	"""Создает задачу в кроне."""
	key = str(b64encode(urandom(6), 'dfsDFAsfsf'))
	opt = [
		conf.BASE_DIR + '/bash/cron_job.sh',
		'-server', ' '.join(selected['servers']),
		'-update', ' '.join(selected['updates']),
		'-date', selected['date'],
		'-cmd', selected['cmd'],
		'-id', key, ]

	kill = '(crontab -l | sed "/' + key + '/d") | crontab -'

	log, err = run_cmd(opt)
	add_event(selected, log, err, key, '')
	add_job(selected, log, key, kill)
	return log, err
