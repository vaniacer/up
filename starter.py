# -*- encoding: utf-8 -*-

from sys import argv
from os import remove
from time import sleep
from getpass import getuser
from subprocess import call
from datetime import datetime
from os.path import join as opj
from importlib import import_module
from argparse import ArgumentParser
from conf import dbname, dbhost, dbpass, dbport, dbuser
from up.settings import LOG_FILE, ERR_FILE, PID_FILE, BASE_DIR, CRON_DIR


parser = ArgumentParser()
parser.add_argument('-H', '--history', help="Save log to history",   action='store_true')
parser.add_argument('-c', '--cron',    help='Set cron job',          action='store_true')
parser.add_argument('--from_cron',     help='Running from cron',     action='store_true')
parser.add_argument('-u', '--update',  help='List of update files',  action='append')
parser.add_argument('-x', '--script',  help='List of script files',  action='append')
parser.add_argument('-o', '--options', help='Custom script options', action='append')
parser.add_argument('-m', '--dump',    help='List of dump files',    action='append')
parser.add_argument('-w', '--wdir',    help="Server's working directory")
parser.add_argument('-s', '--server',  help="Server's ssh address")
parser.add_argument('-P', '--port',    help="Server's port")
parser.add_argument('-d', '--date',    help='Cron job date')
parser.add_argument('-n', '--proname', help='Project name')
parser.add_argument('cmd',             help='Command name')
parser.add_argument('-j', '--job',     help='Cron job id')
parser.add_argument('-k', '--key',     help='Unique key')
parser.add_argument('-p', '--proid',   help='Project id')
args = parser.parse_args()

command = import_module('modules.%s' % args.cmd)
errfile = ERR_FILE + args.key
pidfile = PID_FILE + args.key
logfile = LOG_FILE + args.key
if args.from_cron:
	logfile = opj(CRON_DIR, args.key)


def add_cron_job():
	save_argv = argv
	save_argv.remove('--cron')
	save_argv.remove('starter.py')
	save_argv.extend(['--from_cron'])
	starter = opj(BASE_DIR, 'starter.py')
	python = opj(BASE_DIR, '../env/bin/python')
	cronfile = opj('/var/spool/cron/crontabs', getuser())
	datetime_object = datetime.strptime(args.date, '%Y-%m-%d %H:%M')

	wraped_command = ["'%s'" % opt for opt in save_argv]  # wrap all arguments with ''
	command = '{python} {starter} {command}'.format(python=python, starter=starter, command=' '.join(wraped_command))
	cronjob = "{top}\n{min} {hur} {day} {mon} * {command}; sed '/{key}/d' -i '{cronfile}'\n{bot}\n".format(
		top='#' + '-' * 28 + '{ job %s start }' % args.key + '-' * 28,
		bot='#' + '-' * 28 + '{  job %s end  }' % args.key + '-' * 28,
		min=datetime_object.minute,
		mon=datetime_object.month,
		hur=datetime_object.hour,
		day=datetime_object.day,
		cronfile=cronfile,
		command=command,
		key=args.key,
	)

	with open(cronfile, 'a') as f:
		f.write(cronjob)


def make_history():
	"""Записывает инфо в базу."""

	with open(logfile) as f:
		log_body = f.read()

	log_body = log_body.decode('utf-8', errors='replace')
	log_size = len(log_body)
	if log_size > 4000:
		log_body = u'{head!s}{first!s}\n...\n{last!s}'.format(
			head='<b>Log is too long to store in history, cutting</b>\n',
			first=log_body[:2000],
			last=log_body[-2000:],
		)

	types = {
		'his': {'tab': 'ups_history', 'col': "uniq = '%s'" % args.key, 'ext': ', exit = %s' % error},
		'job': {'tab': 'ups_job',     'col': "cron = '%s'" % args.key, 'ext': ''},
	}

	update = u'UPDATE {tab} SET "desc" = $$ {log} $${ext} WHERE {col};'.format(
		col=types['his']['col'],
		tab=types['his']['tab'],
		ext=types['his']['ext'],
		log=log_body,
	)

	if args.cron:
		update += u'UPDATE {tab} SET "desc" = $$ {log} $${ext} WHERE {col};'.format(
			col=types['job']['col'],
			tab=types['job']['tab'],
			ext=types['job']['ext'],
			log=log_body,
		)

	psql_opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', update]
	his_error = call(psql_opt, env={"PGPASSWORD": dbpass})
	return his_error


error = 0
with open(logfile, 'a') as log:
	if args.cron:
		command.description(args, log)
		add_cron_job()
	else:
		cmd_error = command.run(args, log)
		if cmd_error > 0:
			error = cmd_error

if args.from_cron:
	with open(logfile, 'a') as log:
		today = datetime.today()
		log.write("\nError: {error}\nDate: {date}".format(date=today.strftime('%Y-%m-%d %H:%M'), error=error))
else:
	if args.history:
		his_error = make_history()
		if his_error > 0:
			error = his_error

	with open(errfile, 'w') as f:
		f.write(str(error))

	sleep(10)
	for f in logfile, errfile:
		try:
			remove(f)
		except OSError:
			continue
