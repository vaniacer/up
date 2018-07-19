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
from up.settings import LOG_FILE, ERR_FILE, PID_FILE, BASE_DIR


parser = ArgumentParser()
parser.add_argument('-u', '--update',  help='List of update files',  action='append')
parser.add_argument('-x', '--script',  help='List of script files',  action='append')
parser.add_argument('-o', '--opts',    help='Custom script options', action='append')
parser.add_argument('-m', '--dump',    help='List of dump files',    action='append')
parser.add_argument('-j', '--job',     help='List of cron job ids')
parser.add_argument('-s', '--server',  help="Server's ssh address")
parser.add_argument('-w', '--wdir',    help="Server's working directory")
parser.add_argument('-P', '--port',    help="Server's port")
parser.add_argument('-d', '--date',    help='Cron job date')
parser.add_argument('-p', '--proid',   help='Project id')
parser.add_argument('-n', '--proname', help='Project name')
parser.add_argument('-c', '--cron',    help='Run in cron',         action='store_true')
parser.add_argument('-H', '--history', help="Save log to history", action='store_true')
parser.add_argument('cmd',             help='Command name')
parser.add_argument('key',             help='Unique key')
args = parser.parse_args()

logfile = LOG_FILE + args.key
errfile = ERR_FILE + args.key
pidfile = PID_FILE + args.key
command = import_module('modules.%s' % args.cmd)


def add_cron_job():
	save_argv = argv
	save_argv.remove('--cron')
	save_argv.remove('starter.py')
	command = ' '.join(save_argv)
	starter = opj(BASE_DIR, 'starter.py')
	python = opj(BASE_DIR, '../env/bin/python')
	cronfile = opj('/var/spool/cron/crontabs', getuser())
	datetime_object = datetime.strptime(args.date, '%Y-%m-%d %H:%M')

	cron_job = "{minute} {hour} {day} {month} * {python} {starter} {command}; sed '/{key}/d' -i '{cronfile}'\n".format(
		minute=datetime_object.minute,
		month=datetime_object.month,
		hour=datetime_object.hour,
		day=datetime_object.day,
		cronfile=cronfile,
		command=command,
		starter=starter,
		python=python,
		key=args.key,
	)

	with open(cronfile, 'a') as f:
		f.write(cron_job)


def make_history():
	"""Записывает инфо в базу."""

	with open(logfile) as hlog:
		log_body = hlog.read()
	num_lines = str.count(log_body, '\n')

	if num_lines > 100:
		splited_log = log_body.split('\n')
		log_body = '{top}{head}{middle}{tail}'.format(
			top='<b>Log is too long to store in history, cutting</b>\n',
			head='\n'.join(splited_log[:50]),
			tail='\n'.join(splited_log[-50:]),
			middle='\n...\n',
		)

	types = {
		'his': {'tab': 'ups_history', 'col': "uniq = '%s'" % args.key, 'ext': ', exit = %s' % error},
		'job': {'tab': 'ups_job',     'col': "cron = '%s'" % args.key, 'ext': ''},
	}

	update = 'UPDATE {tab} SET "desc" = $$ {log} $${ext} WHERE {col};'.format(
		col=types['his']['col'],
		tab=types['his']['tab'],
		ext=types['his']['ext'],
		log=log_body,
	)

	if args.cron:
		update += 'UPDATE {tab} SET "desc" = $$ {log} $${ext} WHERE {col};'.format(
			col=types['job']['col'],
			tab=types['job']['tab'],
			ext=types['job']['ext'],
			log=log_body,
		)

	psql_opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', update]
	his_error = call(psql_opt, env={"PGPASSWORD": dbpass})
	return his_error


error = 0
log = open(logfile, 'a')

if args.cron:
	command.description(args, log)
	add_cron_job()
else:
	cmd_error = command.run(args, log)
	if cmd_error > 0:
		error = cmd_error

log.close()

if args.history:
	his_error = make_history()
	if his_error > 0:
				error = his_error

with open(errfile, 'w') as f:
	f.write(str(error))

sleep(10)
for f in logfile, errfile, pidfile:
	try:
		remove(f)
	except OSError:
		continue
