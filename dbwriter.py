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
	log_body = '{head!s}{first!s}\n...\n{last!s}'.format(
		head='<b>Log is too long to store in history, cutting</b>\n',
		first='\n'.join(splited[:50]),
		last='\n'.join(splited[-50:]),
	)

types = {
	'his': {'tab': 'ups_history', 'col': "uniq = '%s'" % key, 'ext': ', exit = %s' % err},
	'job': {'tab': 'ups_job',     'col': "cron = '%s'" % key, 'ext': ''},
}

update = 'UPDATE {tab} SET "desc" = $$ {log!s} $${ext} WHERE {col};'.format(
	col=types[typ]['col'],
	tab=types[typ]['tab'],
	ext=types[typ]['ext'],
	log=log_body,
)

opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', update]
Popen(opt, env={"PGPASSWORD": dbpass})

# Variant with psycopg2, but my is slightly faster
# import psycopg2
# # Connect to an existing database
# conn = psycopg2.connect(host=dbhost, port=dbport, dbname=dbname, user=dbuser, password=dbpass)
# cur = conn.cursor()  # Open a cursor to perform database operations
#
# # Execute a command: update
# cur.execute(u'UPDATE {tab} SET "desc" = $$ {log} $${ext} WHERE {col};'.format(
# 	col=types[typ]['col'],
# 	tab=types[typ]['tab'],
# 	ext=types[typ]['ext'],
# 	log=log_body,
# ))
#
# conn.commit()  # Make the changes to the database persistent
# cur.close()    # Close communication
# conn.close()   # with the database
