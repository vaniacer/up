# -*- encoding: utf-8 -*-

from cron import find_job, cronfile
from popen_call import my_call, message


def description(args, log):
	email = args.email[0]
	log.write('\nSend log to {email} when job {job} finished\n'.format(job=args.job, email=email))


def run(args, log):
	error = 0
	job, jobid = find_job(args.job)
	# add --email {email} to job's args
	email = args.email[0]
	new_job = '{start} --email {email} {end}'.format(start=' '.join(job[:7]), email=email, end=' '.join(job[7:]))
	message('\nEmail to {email} when job {job} finished\n'.format(job=args.job, email=email), log)
	command = ['sed', '/{id}/c{new}'.format(id=jobid, new=new_job), '-i', cronfile]
	error += my_call(command, log)

	return error
