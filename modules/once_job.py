# -*- encoding: utf-8 -*-

from re import escape
from psql import psql
from datetime import datetime
from cron import find_job, cronfile
from popen_call import my_call, message


def description(args, log):
	log.write('\nMake cron job {job} run once\n'.format(job=args.job))


def run(args, log):

	error = 0
	job, jobid = find_job(args.job)
	datetime_object = datetime.strptime(args.date, '%Y-%m-%d %H:%M')
	job[3] = datetime_object.month  # change month and day to current
	job[2] = datetime_object.day    # or to selected date\time
	new_job = ' '.join(escape(str(opt)) for opt in job)
	new_job += "; sed '/{key}/d' \-i '{cronfile}'".format(cronfile=cronfile, key=args.job)  # add cancel command
	print job[0], job[1]
	message('\nSet job {job} to run once\n'.format(job=args.job), log)
	command = ['sed', '/{id}/c{new}'.format(id=jobid, job=args.job, new=new_job), '-i', cronfile]
	sql = "UPDATE ups_job SET cdat = '{date} {H}:{M}', perm = false WHERE cron = '{job}';".format(
		date=args.date.split()[0],
		job=args.job,
		H=job[1],
		M=job[0],
	)
	error += my_call(command, log)
	error += psql(sql)

	return error
