# -*- encoding: utf-8 -*-

from re import escape
from datetime import datetime
from cron import find_job, cronfile
from popen_call import my_call, message


def description(args, log):
	log.write('\nMake cron job {job} run once\n'.format(job=args.job))


def run(args, log):

	job, jobid = find_job(args.job)
	datetime_object = datetime.strptime(args.date, '%Y-%m-%d %H:%M')
	job[3] = datetime_object.month  # change month and day to current
	job[2] = datetime_object.day    # or to selected date\time
	new_job = ' '.join(escape(str(opt)) for opt in job)
	new_job += "; sed '/{key}/d' \-i '{cronfile}'".format(cronfile=cronfile, key=args.job)  # add cancel command

	message('\nSet job {job} to run once\n'.format(job=args.job), log)
	command = ['sed', '/{id}/c{new}'.format(id=jobid, job=args.job, new=new_job), '-i', cronfile]
	error = my_call(command, log)
	return error
