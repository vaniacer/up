# -*- encoding: utf-8 -*-

from popen_call import message
from crontab import CronTab
from getpass import getuser


def description(args, log):
	log.write('\nCancel cron job {job}\n'.format(job=args.job))


def run(args, log):

	message('\nCancel cron job {job}\n'.format(job=args.job), log)

	try:
		cron = CronTab(user=getuser())
		cron.remove_all(comment=args.job)
		cron.write()
		error = 0
	except:
		error = 1

	return error
