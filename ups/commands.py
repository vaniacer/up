# -*- encoding: utf-8 -*-

from .commands_engine import cron_job, run_now, del_job


def commands(selected):
	"""Определяет команду."""
	command = ''.join(selected['command'])

	if selected['cron']:
		runcron, url = cron_job, '#updates_servers'
	else:
		runcron, url = run_now, ''

	cmd = {
		'Copy':          {'cmd': runcron, 'name': 'copy',          'url': url,     'history': 'true'},
		'Update':        {'cmd': runcron, 'name': 'update',        'url': url,     'history': 'true'},
		'Restart':       {'cmd': runcron, 'name': 'restart',       'url': url,     'history': 'true'},
		'Check updates': {'cmd': run_now, 'name': 'check_updates', 'url': url,     'history': ''},
		'Check logs':    {'cmd': run_now, 'name': 'check_logs',    'url': url,     'history': ''},
		'Delete job':    {'cmd': del_job, 'name': 'delete_job',    'url': '#cron', 'history': 'true'}, }

	selected['history'] = cmd[command]['history']
	selected['cmdname'] = cmd[command]['name']
	return cmd[command]['cmd'], cmd[command]['url']
