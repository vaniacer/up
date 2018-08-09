# -*- encoding: utf-8 -*-

from getpass import getuser
from os.path import join as opj
from popen_call import my_call, message


def description(args, log):
	log.write('\nCancel cron job {job}\n'.format(job=args.job))


def run(args, log):

	cronfile = opj('/var/spool/cron/crontabs', getuser())
	message('\nCancel cron job {job}\n'.format(job=args.job), log)
	command = ['sed', '/%s/d' % args.job, '-i', cronfile]
	error = my_call(command, log)
	return error
