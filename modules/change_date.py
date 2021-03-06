# -*- encoding: utf-8 -*-

from re import escape
from psql import psql
from datetime import datetime
from cron import find_job, cronfile
from popen_call import my_call, message


def description(args, log):
	log.write('\nChange run date and time for job {job}\n'.format(job=args.job))


def run(args, log):

	error = 0
	job, jobid = find_job(args.job)
	new_command = ' '.join(escape(opt) for opt in job[4:])
	datetime_object = datetime.strptime(args.date, '%Y-%m-%d %H:%M')
	new_job = '{min} {hur} {day} {mon} {job}'.format(
		min=datetime_object.minute,
		mon=datetime_object.month,
		hur=datetime_object.hour,
		day=datetime_object.day,
		job=new_command,
	)

	message('\nChange run date and time for job {job}\n'.format(job=args.job), log)
	command = ['sed', "/{id}/c{new}".format(id=jobid, new=new_job), '-i', cronfile]
	sql = "UPDATE ups_job SET cdat = '{date}' WHERE cron = '{job}';".format(date=args.date, job=args.job)
	error += my_call(command, log)
	error += psql(sql)

	return error
