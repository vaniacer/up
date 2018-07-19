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
with open(log_filename) as f:
	log_body = f.read()

log_body = log_body.decode('utf-8', errors='replace')
log_size = len(log_body)
if log_size > 4000:
	log_body = u'{head!s}{first!s}\n...\n{last!s}'.format(
		head='<b>Log is too long to store in history, cutting</b>\n',
		first=log_body[:2000],
		last=log_body[-2000:],
	)

types = {
	'his': {'tab': 'ups_history', 'col': "uniq = '%s'" % key, 'ext': ', exit = %s' % err},
	'job': {'tab': 'ups_job',     'col': "cron = '%s'" % key, 'ext': ''},
}

update = u'UPDATE {tab} SET "desc" = $$ {log} $${ext} WHERE {col};'.format(
	col=types[typ]['col'],
	tab=types[typ]['tab'],
	ext=types[typ]['ext'],
	log=log_body,
)

opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', update]
Popen(opt, env={"PGPASSWORD": dbpass})
