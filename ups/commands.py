# -*- encoding: utf-8 -*-


def command(selected):
	"""Определяет команду."""
	cmd = ''.join(selected['command'])

#                         +------------------+-----------------------------+----------------+
#                         | write history    | bash command name           | html tags in   |
#                         | log or not       |                             | output         |
	dick = {            # +------------------+-----------------------------+----------------+

		'Stop':            {'history':  True, 'bash': 'stop.sh',            'tag': False, },
		'Copy':            {'history':  True, 'bash': 'copy.sh',            'tag': False, },
		'Start':           {'history':  True, 'bash': 'start.sh',           'tag': False, },
		'script':          {'history':  True, 'bash': 'script.sh',          'tag': False, },
		'cutils':          {'history':  True, 'bash': 'cutils.sh',          'tag': False, },
		'Update':          {'history':  True, 'bash': 'update.sh',          'tag': False, },
		'Reload':          {'history':  True, 'bash': 'reload.sh',          'tag': False, },
		'Restart':         {'history':  True, 'bash': 'restart.sh',         'tag': False, },
		'delallup':        {'history':  True, 'bash': 'delallup.sh',        'tag': False, },
		'delselup':        {'history':  True, 'bash': 'delselup.sh',        'tag': False, },
		'Get_dump':        {'history':  True, 'bash': 'get_dump.sh',        'tag':  True, },
		'Delete_job':      {'history':  True, 'bash': 'delete_job.sh',      'tag': False, },
		'Check_logs':      {'history': False, 'bash': 'check_logs.sh',      'tag': False, },
		'Check_conf':      {'history': False, 'bash': 'check_conf.sh',      'tag': False, },
		'Check_updates':   {'history': False, 'bash': 'check_updates.sh',   'tag': False, },
		'Maintenance_ON':  {'history':  True, 'bash': 'maintenance_on.sh',  'tag': False, },
		'Maintenance_OFF': {'history':  True, 'bash': 'maintenance_off.sh', 'tag': False, },
	}

	selected['cmdname'] = dick[cmd]['bash']
	selected['history'] = dick[cmd]['history']
	return dick[cmd]['tag'], selected['history']
