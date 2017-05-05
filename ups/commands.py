# -*- encoding: utf-8 -*-


def command(selected):
	"""Определяет команду."""
	cmd = ''.join(selected['command'])
	url = ''  # #cron, #upser, #history

#                         +------------------+-----------------------------+-------------------+
#                         | write history    | bash command name           | url after command |
#                         | log or not       |                             | not working yet ( |
	dick = {            # +------------------+-----------------------------+-------------------+
		'Stop':            {'history': True,  'bash': 'stop.sh',            'url': url, },
		'Copy':            {'history': True,  'bash': 'copy.sh',            'url': url, },
		'Start':           {'history': True,  'bash': 'start.sh',           'url': url, },
		'Update':          {'history': True,  'bash': 'update.sh',          'url': url, },
		'Reload':          {'history': True,  'bash': 'reload.sh',          'url': url, },
		'Restart':         {'history': True,  'bash': 'restart.sh',         'url': url, },
		'Get_dump':        {'history': True,  'bash': 'get_dump.sh',        'url': url, },
		'Delete_job':      {'history': True,  'bash': 'delete_job.sh',      'url': url, },
		'Check_logs':      {'history': False, 'bash': 'check_logs.sh',      'url': url, },
		'Check_updates':   {'history': False, 'bash': 'check_updates.sh',   'url': url, },
		'Maintenance_ON':  {'history': True,  'bash': 'maintenance_on.sh',  'url': url, },
		'Maintenance_OFF': {'history': True,  'bash': 'maintenance_off.sh', 'url': url, },
	}

	selected['cmdname'] = dick[cmd]['bash']
	selected['history'] = dick[cmd]['history']
	return dick[cmd]['url'], selected['history']
