# -*- encoding: utf-8 -*-

from getpass import getuser
from os.path import join as opj


cronfile = opj('/var/spool/cron/crontabs', getuser())


def find_job(key):

	job = []
	jobid = "'--key' '%s'" % key
	with open(cronfile) as f:
		for line in f:
			if jobid in line:
				line = line.strip()
				job = line.split(' ')
				break

	return job, jobid
