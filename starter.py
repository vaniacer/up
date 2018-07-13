# -*- encoding: utf-8 -*-

import os
import time
import argparse
import importlib
from subprocess import Popen
from up.settings import LOG_FILE, ERR_FILE, PID_FILE, DUMP_DIR
from conf import dbname, dbhost, dbpass, dbport, dbuser


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update',  help='List of update files',  action='append')
parser.add_argument('-x', '--script',  help='List of script files',  action='append')
parser.add_argument('-o', '--opts',    help='Custom script options', action='append')
parser.add_argument('-m', '--dump',    help='List of dump files',    action='append')
parser.add_argument('-j', '--job',     help='List of cron job ids',  action='append')
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
command = importlib.import_module('modules.%s' % args.cmd)


def make_history(typ):
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
		col=types[typ]['col'],
		tab=types[typ]['tab'],
		ext=types[typ]['ext'],
		log=log_body,
	)

	psql_opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', update]
	Popen(psql_opt, env={"PGPASSWORD": dbpass})


def download_file(download, log):
	"""Закачка файлов."""

	dump_dir = DUMP_DIR
	files = ' '.join(download['file'])

	if download['dest']:
		dump_dir = os.path.join(DUMP_DIR, download['dest'])

	try:
		os.mkdir(dump_dir)
	except OSError:
		pass

	rsync_opt = [
		'rsync', '--progress', '-lzuogthvr',
		'{addr}:{files}'.format(addr=args.server, files=files), dump_dir,
	]

	if download['kill']:
		rsync_opt.extend(['--remove-source-files'])

	rsync = Popen(rsync_opt, stdout=log, stderr=log)
	rsync.communicate()
	error = rsync.returncode
	rsync.wait()
	return error


def upload_file(upload, log):

	list_of_files = upload['file']
	destination = upload['dest']

	rsync_opt = ['rsync', '--progress', '-lzuogthvr']
	rsync_opt.extend(list_of_files)
	rsync_opt.extend(['{addr}:{dest}/'.format(dest=destination, addr=args.server)])

	rsync = Popen(rsync_opt, stdout=log, stderr=log)
	rsync.communicate()
	error = rsync.returncode
	rsync.wait()
	return error


error = 0
if args.cron:
	with open(logfile, 'w') as f:
		f.write(command.description(args))
	make_history('job')
else:
	dick = command.run(args)
	try:
		upload = dick['upload']
	except KeyError:
		upload = ''

	try:
		download = dick['download']
	except KeyError:
		download = ''

	# Head massage
	with open(logfile, 'w') as f:
		f.write(dick['message']['top'])

	# Start logging
	log = open(logfile, 'a')

	# Upload some files if needed
	if upload:
		upload_error = upload_file(upload, log)
		if upload_error > 0:
			error = upload_error

	# Run command
	run_command = Popen(dick['command'], stdout=log, stderr=log)
	run_command.communicate()
	cmd_error = run_command.returncode
	if cmd_error > 0:
		error = cmd_error
	ppid = run_command.pid
	run_command.wait()

	with open(pidfile, 'w') as f:
		f.write(str(ppid))

	# Download some files if needed
	if download:
		download_error = download_file(download, log)
		if download_error > 0:
			error = download_error

	# Final message
	log.write(dick['message']['bot'])

	with open(errfile, 'w') as f:
		f.write(str(error))

	log.close()

if args.history:
	make_history('his')

time.sleep(10)
for f in logfile, errfile, pidfile:
	try:
		os.remove(f)
	except OSError:
		continue
