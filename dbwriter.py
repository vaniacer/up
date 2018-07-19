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
log_size = len(log_body)

if log_size > 2000:
	log_body = '{head!s}{first!s}\n...\n{last!s}'.format(
		head='<b>Log is too long to store in history, cutting</b>\n',
		first=log_body[:1000],
		last=log_body[-1000:],
	)

types = {
	'his': {'tab': 'ups_history', 'col': "uniq = '%s'" % key, 'ext': ', exit = %s' % err},
	'job': {'tab': 'ups_job',     'col': "cron = '%s'" % key, 'ext': ''},
}

update = 'UPDATE {tab} SET "desc" = $$ {log} $${ext} WHERE {col};'.format(
	col=types[typ]['col'],
	tab=types[typ]['tab'],
	ext=types[typ]['ext'],
	log=log_body,
)

opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', update]
Popen(opt, env={"PGPASSWORD": dbpass})
