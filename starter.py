# -*- encoding: utf-8 -*-

import os
import sys
import time
import argparse
import importlib
from subprocess import Popen
from up.settings import LOG_FILE, ERR_FILE, PID_FILE, DUMP_DIR
from conf import dbname, dbhost, dbpass, dbport, dbuser


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update',  help='List of update files')
parser.add_argument('-x', '--script',  help='List of script files')
parser.add_argument('-o', '--opts',    help='Custom script options')
parser.add_argument('-m', '--dump',    help='List of dump files')
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

try:
	imp = importlib.import_module('modules.%s' % args.cmd)
except ImportError:
	print 'No such module'
	sys.exit(1)

log_filename = LOG_FILE + args.key
err_filename = ERR_FILE + args.key
pid_filename = PID_FILE + args.key


def make_history(typ):
	"""Записывает инфо в базу."""

	with open(log_filename) as hlog:
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


def download(ddick, dlog):
	"""Закачка файлов."""

	dump_dir = DUMP_DIR
	filepath = ddick['path']

	if ddick['dest']:
		dump_dir = os.path.join(DUMP_DIR, ddick['dest'])

	try:
		os.mkdir(dump_dir)
	except OSError:
		pass

	rsync_opt = [
		'rsync', '-e', 'ssh', '--progress', '-lzuogthvr',
		'{addr}:"{file}"'.format(addr=args.server, file=filepath), dump_dir
	]

	Popen(rsync_opt, stdout=dlog, stderr=dlog).wait()


if args.cron:
	with open(log_filename, 'w') as log:
		log.write(imp.description(args))
	make_history('job')
else:
	dick = imp.run(args)
	with open(log_filename, 'w') as log:
		log.write(dick['message']['top'])

	log = open(log_filename, 'a')
	run_command = Popen(dick['command'], stdout=log, stderr=log)
	streamdata = run_command.communicate()
	error = run_command.returncode
	ppid = run_command.pid
	run_command.wait()

	if dick['download']:
		download(dick['download'], log)

	log.write(dick['message']['bot'])

	with open(err_filename, 'w') as errlog:
		errlog.write(str(error))

	with open(pid_filename, 'w') as pidlog:
		pidlog.write(str(ppid))

	log.close()

if args.history:
	make_history('his')

time.sleep(10)
for f in log_filename, err_filename, pid_filename:
	try:
		os.remove(f)
	except OSError:
		continue
