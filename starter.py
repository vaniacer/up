# -*- encoding: utf-8 -*-

import os
import sys
import time
import argparse
import importlib
from subprocess import Popen
from up.settings import LOG_FILE, ERR_FILE, PID_FILE
from conf import dbname, dbhost, dbpass, dbport, dbuser


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update',  help='List of update files')
parser.add_argument('-x', '--script',  help='List of script files')
parser.add_argument('-o', '--opts',    help='Custom script options')
parser.add_argument('-m', '--dump',    help='List of dump files')
parser.add_argument('-j', '--job',     help='List of cron job ids')
parser.add_argument('-s', '--server',  help='Server')
parser.add_argument('-w', '--wdir',    help="Server's working directory")
parser.add_argument('-P', '--port',    help="Server's port")
parser.add_argument('-d', '--date',    help='Cron job date')
parser.add_argument('-c', '--cron',    help='Run in cron')
parser.add_argument('-p', '--project', help='Run in cron')
parser.add_argument('-H', '--history', action='store_true', help="Save log to history")
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

	log_body = open(log_filename, 'r').read()
	num_lines = str.count(log_body, '\n')

	if num_lines > 100:
		splited = log_body.split('\n')
		log_body = '{head}{first}{middle}{last}'.format(
			head='<b>Log is too long to store in history, cutting</b>\n',
			first='\n'.join(splited[:50]),
			last='\n'.join(splited[-50:]),
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


if args.cron:
	log = open(log_filename, 'w')
	log.write(imp.description(args))
	make_history('job')
	log.close()
else:
	command, message = imp.run(args)
	log = open(log_filename, 'w')
	log.write(message)
	log.close()

	log = open(log_filename, 'a')

	opt = ['ssh', args.server]
	opt.extend(command)

	run_command = Popen(opt, stdout=log, stderr=log)
	streamdata = run_command.communicate()[0]
	error = run_command.returncode
	ppid = run_command.pid

	log.close()

	err = open(err_filename, 'w')
	err.write(str(error))
	err.close()

	pid = open(pid_filename, 'w')
	pid.write(str(ppid))
	pid.close()

	if args.history:
		make_history('his')

time.sleep(10)
for f in log_filename, err_filename, pid_filename:
	try:
		os.remove(f)
	except OSError:
		continue
