# -*- encoding: utf-8 -*-

from getpass import getuser
from os.path import join as opj


cronfile = opj('/var/spool/cron/crontabs', getuser())


def find_job(id):
	with open(cronfile) as f:
		for line in f:
			if '--key %s' % id in line:
				line = line.strip()
				job = line.split(' ')
				return job
