# -*- encoding: utf-8 -*-

from re import sub
from sys import argv
from os import remove
from os.path import exists
from argparse import Namespace
from modules.psql import regular_log
from modules.log_cutter import log_cutter
from subprocess import call, check_output
from up.settings import LOG_FILE, ERR_FILE


error = 1
keys = argv[1::]
kill = ['kill', '-9']
pids_raw = check_output(['ps', 'a', '-o', 'pid,cmd'])
pids_raw = sub('.*killer.py.*', '', pids_raw)
pid_list = pids_raw.split('\n')

for key in keys:
	logfile = LOG_FILE + key
	errfile = ERR_FILE + key
	arg = Namespace(key=key, cron=False)

	kill.extend([s.lstrip().split(' ')[0] for s in pid_list if key in s])

	if exists(logfile):
		with open(logfile) as f:
			fullog = f.read()
		log = log_cutter(fullog)
		regular_log(arg, error, log)

	for f in logfile, errfile:
		if exists(f):
			remove(f)

call(kill)
