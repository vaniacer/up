# -*- encoding: utf-8 -*-

from django.conf import settings as conf
from subprocess import Popen, PIPE
from .buttons import add_event
import re
import os


crondir = os.path.join(conf.BASE_DIR, '../logs/cron/')


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
	run = Popen(opt, stdout=PIPE)
	out = run.communicate()  # Returns tuple

	for line in out[0].split('\n'):
		if line:
			job = Job('', '', '', '', '')

			# Format time\date
			raw = line.split()
			mnt = raw[0]
			hrs = raw[1]
			day = raw[2]
			mon = raw[3]

			# Get list of servers\updates
			updates = re.sub('^.*-u "', '', line)
			updates = re.sub('" -s .*$', '', updates)
			updates = re.sub(' ', '\n', updates)
			servers = re.sub('^.*-s "', '', line)
			servers = re.sub('".*$', '', servers)
			servers = re.sub(' ', '\n', servers)

			job.full = line
			job.name = re.sub('^.*-cron ', '', line)
			job.name = re.sub(';.*$', '', job.name)
			job.kill = re.sub('^.*; ', '', line)
			job.date = day + '.' + mon + ' ' + hrs + ':' + mnt
			job.desc = 'Copy Updates: \n' + updates + '\n\n' + 'to Servers: \n' + servers

			jobs.append(job)

	return jobs


def get_cron_logs(project):
	"""Создает события в истории на основе логов крона."""

	logfiles = os.listdir(crondir)

	if logfiles:

		history = project.history_set.order_by('date').reverse()

		for filename in logfiles:
			event = history.filter(cron=str(filename))[0]

			f = open(os.path.join(crondir, filename), 'r')
			out = f.readlines()
			f.close()

			err = out[-1]
			err = re.sub('Error: ', '', err)

			date = out[-2]
			date = re.sub('Date: ', '', date)

			del out[-2:]
			out = ''.join(out)

			name = re.sub('Set', 'Run', event.name)

			add_event(event.proj, event.user, name, out, int(err), event.cron, date)
			os.remove(os.path.join(crondir, filename))
