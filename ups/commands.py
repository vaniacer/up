# -*- encoding: utf-8 -*-

from .commands_engine import cron_job, run_now, del_job


def commands(selected):

	command = ''.join(selected['command'])

	if selected['cron']:
		runcron, url = cron_job, '#updates_servers'
	else:
		runcron, url = run_now, ''

	cmd = {
		'copy':          {'cmd': runcron,  'url': url,     'history': 'true'},
		'update':        {'cmd': runcron,  'url': url,     'history': 'true'},
		'restart':       {'cmd': runcron,  'url': url,     'history': 'true'},
		'check_updates': {'cmd': run_now,  'url': url,     'history': ''},
		'check_logs':    {'cmd': run_now,  'url': url,     'history': ''},
		'delete_job':    {'cmd': del_job,  'url': '#cron', 'history': 'true'}, }

	selected['history'] = cmd[command]['history']
	return cmd[command]['cmd'], cmd[command]['url']
