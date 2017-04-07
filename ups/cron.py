# -*- encoding: utf-8 -*-

from django.conf import settings as conf
from subprocess import Popen, PIPE
from .buttons import add_event
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
	run = Popen(opt, stdout=PIPE)
	out = run.communicate()[0]  # Returns tuple

	for line in out.split('\n'):
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
			command = re.sub('^.*bash/', '', line)
			command = re.sub('.sh.*$', '', command)

			# Job's details
			job.full = line
			job.name = re.sub('^.*-cron ', '', line)
			job.name = re.sub(';.*$', '', job.name)
			job.kill = re.sub('^.*; ', '', line)
			job.date = day + '.' + mon + ' ' + hrs + ':' + mnt
			if command == 'copy':
				job.desc = 'Copy Update(s): \n' + updates + '\n\n' + 'to Server(s): \n' + servers

			if command == 'update':
				job.desc = 'Update server(s): \n' + servers + '\n\n' + 'with update(s): \n' + updates

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

			name = re.sub('Set', 'Run', event.name)

			add_event(event.proj, event.user, name, out, int(err), event.cron, date)
			os.remove(os.path.join(conf.CRON_DIR, filename))
