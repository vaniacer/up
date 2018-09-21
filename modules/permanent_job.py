# -*- encoding: utf-8 -*-

from re import sub
from pg_writer import psql
from cron import find_job, cronfile
from popen_call import my_call, message


def description(args, log):
	log.write('\nMake cron job {job} run everyday\n'.format(job=args.job))


def run(args, log):

	job, jobid = find_job(args.job)
	job[3] = '*'  # change month and day
	job[2] = '*'  # to * (everyday)
	new_job = ' '.join(job)  # no need to escape coz sub do it
	new_job = sub(';.*$', '', new_job)  # cut cancel command

	message('\nSet job {job} to run everyday\n'.format(job=args.job), log)
	command = ['sed', '/{id}/c{new}'.format(id=jobid, job=args.job, new=new_job), '-i', cronfile]
	sql = "UPDATE ups_job SET cdat = 'Everyday {time}', perm = true WHERE cron = '{job}';".format(
		time=args.date.split()[-1],
		job=args.job
	)
	error = my_call(command, log)
	error += psql(sql)

	return error
