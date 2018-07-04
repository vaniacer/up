# -*- encoding: utf-8 -*-

import sys
import django
django.setup()
from ups.models import History, Job
from django.conf import settings as conf

typ = sys.argv[1]
key = sys.argv[2]
try:
	err = sys.argv[3]
except IndexError:
	err = None

log_filename = conf.LOG_FILE + key
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

object_to_change = None
if typ == 'his':
	object_to_change = History.objects.get(uniq=key)
if typ == 'job':
	object_to_change = Job.objects.get(cron=key)

object_to_change.desc = log_body
if err:
	object_to_change.exit = err
object_to_change.save()
