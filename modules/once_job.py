# -*- encoding: utf-8 -*-

from re import escape
from datetime import datetime
from cron import find_job, cronfile
from popen_call import my_call, message


def description(args, log):
	log.write('\nMake cron job {job} run once\n'.format(job=args.job))


def run(args, log):

	job = find_job(args.job)
	new_command = ' '.join(escape(opt) for opt in job[4:])
	datetime_object = datetime.strptime(args.date, '%Y-%m-%d %H:%M')
	new_job = '{min} {hur} {day} {mon} {job}'.format(
		min=datetime_object.minute,
		mon=datetime_object.month,
		hur=datetime_object.hour,
		day=datetime_object.day,
		job=new_command,
	)

	message('\nSet job {job} to run once\n'.format(job=args.job), log)
	command = ['sed', '/\-\-key {job}/c{new}'.format(job=args.job, new=new_job), '-i', cronfile]
	error = my_call(command, log)
	return error
