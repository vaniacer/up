# -*- encoding: utf-8 -*-

from sys import argv
from os import remove
from re import findall
from os.path import exists
from argparse import Namespace
from up.settings import LOG_FILE
from modules.psql import regular_log
from modules.log_cutter import log_cutter
from subprocess import call, check_output


error = 1
keys = argv[1::]
kill = ['kill', '-9']
pids_raw = check_output(['ps', '-eo', 'pid,cmd'])
pid_list = findall('.*starter.py.*', pids_raw)

for key in keys:
	logfile = LOG_FILE + key
	arg = Namespace(key=key, cron=False)

	pids = [s.split()[0] for s in pid_list if key in s]
	if pids:
		kill.extend(pids)
		call(kill)

	if exists(logfile):
		with open(logfile) as f:
			log = f.read()
		log = log_cutter(log)
		log += '\n<b>Interrupted...</b>'
		regular_log(arg, error, log)

	if exists(logfile):
		remove(logfile)
