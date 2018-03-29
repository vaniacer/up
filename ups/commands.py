# -*- encoding: utf-8 -*-

from .commands_engine import get_key, starter, add_event, add_job
from .permissions import check_perm
import datetime


def command(selected):
	"""Определяет bash script по полученному command name."""
	dick = {
		#                 +------------------+-----------------------------+----------------+
		#                 |  Write history   |  Bash script names          |  Html tags in  |
		#                 |  log or not      |                             |  output        |
		# RUN only        +------------------+-----------------------------+----------------+
		'check_updates':   {'history': False, 'bash':   'check_updates.sh', 'tag': False, },
		'server_info':     {'history': False, 'bash':     'server_info.sh', 'tag':  True, },
		'check_conf':      {'history': False, 'bash':      'check_conf.sh', 'tag': False, },
		'check_logs':      {'history': False, 'bash':      'check_logs.sh', 'tag': False, },
		'cancel_job':      {'history':  True, 'bash':  'cronjob_cancel.sh', 'tag': False, },
		'permanent_job':   {'history':  True, 'bash':    'cronjob_perm.sh', 'tag': False, },
		'once_job':        {'history':  True, 'bash':    'cronjob_once.sh', 'tag': False, },
		'get_logs_all':    {'history': False, 'bash':    'logs_get_all.sh', 'tag':  True, },
		'get_logs_day':    {'history': False, 'bash':    'logs_get_day.sh', 'tag':  True, },
		'tunnel':          {'history': False, 'bash':          'tunnel.sh', 'tag':  True, },
		# Maintenance     +------------------+-----------------------------+----------------+
		'stop':            {'history':  True, 'bash':            'stop.sh', 'tag': False, },
		'start':           {'history':  True, 'bash':           'start.sh', 'tag': False, },
		'reload':          {'history':  True, 'bash':          'reload.sh', 'tag': False, },
		'restart':         {'history':  True, 'bash':         'restart.sh', 'tag': False, },
		'maintenance_on':  {'history':  True, 'bash':  'maintenance_on.sh', 'tag': False, },
		'maintenance_off': {'history':  True, 'bash': 'maintenance_off.sh', 'tag': False, },
		# Delete updates  +------------------+-----------------------------+----------------+
		'del_sel_updates': {'history':  True, 'bash': 'del_sel_updates.sh', 'tag': False, },
		'del_all_updates': {'history':  True, 'bash': 'del_all_updates.sh', 'tag': False, },
		# Dumps           +------------------+-----------------------------+----------------+
		'get_dump':        {'history':  True, 'bash':        'dump_get.sh', 'tag':  True, },
		'send_dump':       {'history':  True, 'bash':       'dump_send.sh', 'tag':  True, },
		'del_dump':        {'history':  True, 'bash':        'dump_del.sh', 'tag': False, },
		# Backup          +------------------+-----------------------------+----------------+
		'backup_db':       {'history':  True, 'bash':       'backup_db.sh', 'tag':  True, },
		'backup_sys':      {'history':  True, 'bash':      'backup_sys.sh', 'tag':  True, },
		'backup_full':     {'history':  True, 'bash':     'backup_full.sh', 'tag':  True, },
		# Main            +------------------+-----------------------------+----------------+
		'copy':            {'history':  True, 'bash':            'copy.sh', 'tag': False, },
		'update':          {'history':  True, 'bash':          'update.sh', 'tag':  True, },
		'copy_utils':      {'history':  True, 'bash':      'copy_utils.sh', 'tag': False, },
		'sql_script':      {'history':  True, 'bash':      'script_sql.sh', 'tag':  True, },
		'bash_script':     {'history':  True, 'bash':     'script_bash.sh', 'tag':  True, },
	}

	cmd = ''.join(selected['command'])
	selected['cmdname'] = dick[cmd]['bash']
	selected['history'] = dick[cmd]['history']
	return dick[cmd]['tag'], selected['history']


def info(data):
	url = ''
	if data.get('server_info'):
		url += '&server_info=on'
	if data.get('script_info'):
		url += '&script_info=on'
	if data.get('update_info'):
		url += '&update_info=on'
	if data.get('dbdump_info'):
		url += '&dbdump_info=on'
	if data.get('servers'):
		url += '&servers=%s' % data.get('servers')
	return url


def run_date():
	"""Если не указана дата, возвращает текущую дату + 1 минута."""
	date = datetime.datetime.now() + datetime.timedelta(minutes=1)
	return date.strftime("%Y-%m-%d %H:%M")


def cmd_run(data, project, user):
	"""Запускает выбранную команду."""
	check_perm('run_command', project, user)

	crn = ''
	key = get_key()
	date = run_date()

	if data['selected_date'] and data['selected_time']:
		date = '%s %s' % (data['selected_date'], data['selected_time'])

	selected = {
		'hid':     '',
		'cid':     '',
		'key':     key,
		'date':    date,
		'user':    user,
		'project': project,
		'rtype':   data['run_type'],
		'name':    data['selected_command'],
		'command': data['selected_command'],
		'cronjbs': data.getlist('selected_jobs'),
		'dumps':   data.getlist('selected_dumps'),
		'updates': data.getlist('selected_updates'),
		'scripts': data.getlist('selected_scripts'),
		'servers': data.getlist('selected_servers'),
	}

	tag, his = command(selected)
	if data['run_type'] == 'CRON':
		crn = key
		selected['cid'] = add_job(selected, '_empty_', key)
		selected['name'] = 'Set cron job - %s' % selected['command'].lower()
	if his:
		selected['hid'] = add_event(selected, '_empty_', 0, crn, date)
	starter(selected)

	url = '/command_log/?cmd=%s&rtype=%s&hid=%s&cid=%s&prid=%s%s&timedate=%s&logid=%s' % (
		data['selected_command'],
		selected['rtype'],
		selected['hid'],
		selected['cid'],
		project.id,
		info(data),
		date,
		key,
	)

	return url
