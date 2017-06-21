# -*- encoding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as conf
from .models import History, Job
from subprocess import Popen
from base64 import b64encode
from os import urandom
from .models import Server as S
from django.shortcuts import get_object_or_404 as gor4


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


def del_job(selected):
	"""Удаляет из базы записи о крон жобах."""
	for i in selected['cronjbs']:
		try:
			Job.objects.get(cron=i).delete()
		except ObjectDoesNotExist:
			continue


# def servers(selected):
# 	obj = []
# 	for i in selected['servers']:
# 		obj.append('%s:%s:%s' % (gor4(S, id=i).addr, gor4(S, id=i).wdir, gor4(S, id=i).port))
# 	return ' '.join(obj)


def starter(selected):
	"""Выполняет комманду."""
	opt = [
		conf.BASE_DIR + '/bash/starter.sh',
		'-prj', str(selected['project'].id),
		'-cmd', selected['cmdname'],
		'-key', selected['key']]

	if selected['servers']:
		opt.extend(['-server', ' '.join(selected['servers'])])
	if selected['updates']:
		opt.extend(['-update', ' '.join(selected['updates'])])
	if selected['cronjbs']:
		del_job(selected)
		opt.extend(['-job', ' '.join(selected['cronjbs'])])
	if selected['cron']:
		opt.extend([
			'-run',  selected['cmdname'],
			'-date', selected['date'],
			'-key',  selected['key'],
			'-id',   selected['key'],
			'-cmd',  'cron.sh'])

	Popen(opt)
