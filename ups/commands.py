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
		'Copy':          {'cmd': runcron, 'history': True,  'bash': 'copy.sh',          'url': url, },
		'Update':        {'cmd': runcron, 'history': True,  'bash': 'update.sh',        'url': url, },
		'Restart':       {'cmd': runcron, 'history': True,  'bash': 'restart.sh',       'url': url, },
		'Delete job':    {'cmd': del_job, 'history': True,  'bash': 'delete_job.sh',    'url': '#cron', },
		'Check logs':    {'cmd': run_now, 'history': False, 'bash': 'check_logs.sh',    'url': url, },
		'Check updates': {'cmd': run_now, 'history': False, 'bash': 'check_updates.sh', 'url': url, }, }

	selected['history'] = cmd[command]['history']
	selected['cmdname'] = cmd[command]['bash']
	return cmd[command]['cmd'], cmd[command]['url']
