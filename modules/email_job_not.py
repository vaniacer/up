# -*- encoding: utf-8 -*-

from re import sub
from cron import find_job, cronfile
from popen_call import my_call, message


def description(args, log):
	email = args.email[0]
	log.write('\nStop sending log to {email} when job {job} finished\n'.format(job=args.job, email=email))


def run(args, log):
	error = 0
	email = args.email[0]
	job, jobid = find_job(args.job)
	new_job = ' '.join(job)
	new_job = sub('--email {email}'.format(email=email), '', new_job)
	message('\nStop sending email to {email} when job {job} finished\n'.format(job=args.job, email=email), log)
	command = ['sed', '/{id}/c{new}'.format(id=jobid, new=new_job), '-i', cronfile]
	error += my_call(command, log)

	return error
