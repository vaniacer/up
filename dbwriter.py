# -*- encoding: utf-8 -*-

import sys
from subprocess import Popen
from up.settings import LOG_FILE
from conf import dbname, dbhost, dbpass, dbport, dbuser


typ = sys.argv[1]
key = sys.argv[2]
try:
	err = sys.argv[3]
except IndexError:
	err = None

log_filename = LOG_FILE + key
log_body = open(log_filename, 'r').read()
num_lines = str.count(log_body, '\n')

if num_lines > 100:
	splited = log_body.split('\n')
	log_body = u'{head!s}{first!s}{midle!s}{last!s}'.format(
		head='<b>Log is too long to store in history, cutting</b>\n',
		first='\n'.join(splited[:50]),
		last='\n'.join(splited[-50:]),
		midle='\n...\n',
	)

update = ''
if typ == 'his':
	update = u'UPDATE ups_history SET ' \
			u'"desc" = $$ {log} $$, ' \
			u'"exit" = $$ {err} $$ ' \
			u'WHERE "uniq" = \'{key}\';'.format(
				log=log_body,
				err=err,
				key=key,
			)
if typ == 'job':
	update = u'UPDATE ups_job SET "desc" = $$ {log} $$ WHERE "cron" = \'{key}\';'.format(
		log=log_body,
		key=key,
	)

opt = [
	'psql',
	'-U', dbuser,
	'-h', dbhost,
	'-p', dbport,
	'-d', dbname,
	'-c', update,
]

Popen(opt, env={"PGPASSWORD": dbpass})

