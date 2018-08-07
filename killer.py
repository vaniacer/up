# -*- encoding: utf-8 -*-

from re import sub
from sys import argv
from os import remove
from subprocess import call, check_output
from up.settings import LOG_FILE, ERR_FILE
from conf import dbname, dbhost, dbpass, dbport, dbuser


def make_log(logfile):
	"""Обрабатывает логи"""
	with open(logfile) as f:
		log_body = f.read()

	log_body += '<b>Interrupted...</b>'
	log_body = log_body.decode('utf-8', errors='replace')
	log_size = len(log_body)
	if log_size > 4000:
		log_body = u'{head!s}{first!s}\n...\n{last!s}'.format(
			head='<b>Log is too long to store in history, cutting</b>\n',
			first=log_body[:2000],
			last=log_body[-2000:],
		)

	return log_body


def make_history():
	"""Записывает инфо в базу"""
	psql_opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', update]
	call(psql_opt, env={"PGPASSWORD": dbpass})


error = 1
update = u''
keys = argv[1::]
command = ['kill']
pids_raw = check_output(['ps', 'a', '-o', 'pid,cmd'])
pids_raw = sub('.*killer.py.*', '', pids_raw)
pid_list = pids_raw.split('\n')

for key in keys:
	logfile = LOG_FILE + key
	errfile = ERR_FILE + key
	log = make_log(logfile)

	update += u'UPDATE {tab} SET "desc" = $$ {log} $$, exit = {ext} WHERE uniq = \'{key}\'; '.format(
		tab='ups_history',
		ext=error,
		log=log,
		key=key,
	)

	command.extend([s.lstrip().split(' ')[0] for s in pid_list if key in s])

	for f in logfile, errfile:
		try:
			remove(f)
		except OSError:
			continue

call(command)
make_history()
