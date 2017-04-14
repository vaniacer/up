# -*- encoding: utf-8 -*-

from .commands_engine import add_event, run_cmd
from django.conf import settings as conf
import re
import os


class Job:
	"""Задания в кроне."""

	def __init__(self, name, full, desc, date, kill):
		self.name = name
		self.full = full
		self.desc = desc
		self.date = date
		self.kill = kill

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


def get_cron_jobs(current_project):
	"""Получает список заданий крона для проекта."""

	jobs = []

	opt = ['bash/cron_list.sh', '-project', current_project.name]
	out, err = run_cmd(opt)

	for line in out.split('\n'):
		if line:
			job = Job('', '', '', '', '')
			raw = line.split()

			# Format time\date
			mnt, hrs, day, mon = raw[0:4]

			# Get job description
			cmd = raw[5]
			upd = line.split('"')[1]
			srv = line.split('"')[3]
			opt = [cmd, '-u', upd, '-s', srv, '-desc', 'true']
			out, err = run_cmd(opt)

			# Job's details
			job.full = line
			job.name = raw[-10]
			job.kill = ' '.join(raw[-8:])
			job.date = day + '.' + mon + ' ' + hrs + ':' + mnt
			job.desc = out

			jobs.append(job)
	return jobs


def get_cron_logs(project):
	"""Создает события в истории на основе логов крона."""

	logfiles = os.listdir(conf.CRON_DIR)

	if logfiles:

		history = project.history_set.order_by('date').reverse()

		for filename in logfiles:
			event = history.filter(cron=str(filename))[0]

			f = open(os.path.join(conf.CRON_DIR, filename), 'r')
			out = f.readlines()
			f.close()

			err = out[-1]
			err = re.sub('Error: ', '', err)
			date = out[-2]
			date = re.sub('Date: ', '', date)

			del out[-2:]
			out = ''.join(out)

			dick = {'project': event.proj, 'user': event.user, 'cmd': event.name}
			add_event(dick, out, int(err), event.cron, date)
			os.remove(os.path.join(conf.CRON_DIR, filename))
