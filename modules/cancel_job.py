# -*- encoding: utf-8 -*-

from popen_call import message

from getpass import getuser


def description(args, log):
	log.write('\nCancel cron job {job}\n'.format(job=args.job))


def run(args, log):

	message('\nCancel cron job {job}\n'.format(job=args.job), log)



	return error
