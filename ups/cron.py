# -*- encoding: utf-8 -*-

from subprocess import Popen, PIPE
import re


class Job:
	"""Задания в кроне."""

	def __init__(self, name, full, desc, date):
		self.name = name
		self.full = full
		self.desc = desc
		self.date = date

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
			raw = line.split()
			job = Job('', '', '', '')

			if 'copy.sh' in line:
				job.name = 'Copy update(s) to server(s)'

			job.full = line
			# Format time\date
			mnt = raw[0]
			hrs = raw[1]
			day = raw[2]
			mon = raw[3]
			job.date = day + '.' + mon + ' ' + hrs + ':' + mnt

			updates = re.sub('^.*-u ', '', line)
			updates = re.sub(' -s .*$', '', updates)
			updates = re.sub(' ', '\n', updates)

			servers = re.sub('^.*-s ', '', line)
			servers = re.sub('; .*$', '', servers)
			servers = re.sub(' ', '\n', servers)

			# Description
			job.desc = 'Servers: \n' + servers + '\n' + 'Updates: \n' + updates

			jobs.append(job)

	return jobs