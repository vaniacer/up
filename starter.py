# -*- encoding: utf-8 -*-

from sys import argv
from os import remove
from time import sleep
from os.path import exists
from getpass import getuser
from subprocess import call
from datetime import datetime
from os.path import join as opj
from importlib import import_module
from argparse import ArgumentParser
from modules.log_cutter import log_cutter
from up.settings import LOG_FILE, BASE_DIR
from modules.psql import cron_log, regular_log

parser = ArgumentParser()
parser.add_argument('-H', '--history', help="Save log to history",   action='store_true')
parser.add_argument('-c', '--cron',    help='Set cron job',          action='store_true')
parser.add_argument('--from_cron',     help='Running from cron',     action='store_true')
parser.add_argument('-u', '--update',  help='List of update files',  action='append')
parser.add_argument('-x', '--script',  help='List of script files',  action='append')
parser.add_argument('-o', '--options', help='Custom script options', action='append')
parser.add_argument('-d', '--dump',    help='List of dump files',    action='append')
parser.add_argument('--email',         help="Email to send log",     action='append')
parser.add_argument('-l', '--limit',   help="Server's rsync speed limit", default=0)
parser.add_argument('-w', '--wdir',    help="Server's working directory")
parser.add_argument('-s', '--server',  help="Server's ssh address")
parser.add_argument('-P', '--port',    help="Server's port")
parser.add_argument('-D', '--date',    help='Cron job date')
parser.add_argument('-n', '--name',    help='Project name')
parser.add_argument('cmd',             help='Command name')
parser.add_argument('-j', '--job',     help='Cron job id')
parser.add_argument('-k', '--key',     help='Unique key')
parser.add_argument('-p', '--pid',     help='Project id')
parser.add_argument('--url',           help='UpS url')
args = parser.parse_args()

command = import_module('modules.%s' % args.cmd)
logfile = LOG_FILE + args.key


def add_cron_job():
	"""Создает запись в кронтабзе"""
	save_argv = argv
	save_argv.remove('--cron')
	save_argv.remove('starter.py')
	save_argv.append('--from_cron')
	starter = opj(BASE_DIR, 'starter.py')
	python = opj(BASE_DIR, '../env/bin/python')
	cronfile = opj('/var/spool/cron/crontabs', getuser())
	datetime_object = datetime.strptime(args.date, '%Y-%m-%d %H:%M')

	wraped_command = ["'%s'" % opt for opt in save_argv]  # wrap all arguments with ''
	command = '{python} {starter} {command}'.format(python=python, starter=starter, command=' '.join(wraped_command))
	cronjob = "{top}\n{min} {hur} {day} {mon} * {command}; sed '/{key}/d' -i '{cronfile}'\n{bot}\n#new {key}".format(
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

	# add this 'magic' to prevent new job freezing
	sed = ['sed', '/#new {}/d'.format(args.key), '-i', cronfile]
	call(sed)


def send_email(message, err):
	"""Отправляет лог на почту"""
	from django.conf import settings
	settings.configure(**locals())
	from django.core.mail import EmailMessage
	status = 'success'
	if err > 0:
		status = 'fail'
	subject = 'Cron job {key} on {srv} {stat}'.format(key=args.key, srv=args.server, stat=status)
	message = '<pre>{mes}</pre>\nКод ошибки: {err}'.format(mes=message, err=err)
	email = EmailMessage(subject, message, to=args.email)
	email.content_subtype = "html"
	email.send()


error = 0
# Run command }------------------------
with open(logfile, 'a') as log:
	if args.cron:
		command.description(args, log)
		add_cron_job()
	else:
		error += command.run(args, log)

# Write logs to DB }-------------------
with open(logfile) as f:
	fullog = f.read()
log = log_cutter(fullog)

if args.from_cron:
	cron_log(args, error, log)
	if args.email:
		send_email(fullog, error)
else:
	regular_log(args, error, log)

# Delete log files }-------------------
sleep(10)
if exists(logfile):
	remove(logfile)
