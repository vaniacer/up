# -*- encoding: utf-8 -*-

from .commands_engine import get_key
from .commands_engine import starter
from .permissions import check_perm
import datetime


def command(selected):
	"""Определяет bash script по полученному command name."""
# ------------------------+------------------+-----------------------------+----------------+----------------
#     --------------------|  Write history   |  Bash script names          |  Html tags in  |------------
	dick = {  # ----------|  log or not      |                             |  output        |--------
		# RUN only |------+------------------+-----------------------------+----------------+---
		'check_updates':   {'history': False, 'bash':   'check_updates.sh', 'tag': False, },
		'server_info':     {'history': False, 'bash':     'server_info.sh', 'tag':  True, },
		'check_conf':      {'history': False, 'bash':      'check_conf.sh', 'tag': False, },
		'check_logs':      {'history': False, 'bash':      'check_logs.sh', 'tag': False, },
		'cancel_job':      {'history':  True, 'bash':  'cronjob_cancel.sh', 'tag': False, },
		'permanent_job':   {'history':  True, 'bash':    'cronjob_perm.sh', 'tag': False, },
		'once_job':        {'history':  True, 'bash':    'cronjob_once.sh', 'tag': False, },
		'get_logs':        {'history': False, 'bash':        'logs_get.sh', 'tag':  True, },
		'tunnel':          {'history': False, 'bash':          'tunnel.sh', 'tag':  True, },

		# Maintenance |----------------------+-----------------------------+----------------+
		'stop':            {'history':  True, 'bash':            'stop.sh', 'tag': False, },
		'start':           {'history':  True, 'bash':           'start.sh', 'tag': False, },
		'reload':          {'history':  True, 'bash':          'reload.sh', 'tag': False, },
		'restart':         {'history':  True, 'bash':         'restart.sh', 'tag': False, },
		'maintenance_on':  {'history':  True, 'bash':  'maintenance_on.sh', 'tag': False, },
		'maintenance_off': {'history':  True, 'bash': 'maintenance_off.sh', 'tag': False, },
		# Delete updates |-------------------+-----------------------------+----------------+
		'del_sel_updates': {'history':  True, 'bash': 'del_sel_updates.sh', 'tag': False, },
		'del_all_updates': {'history':  True, 'bash': 'del_all_updates.sh', 'tag': False, },
		# Dumps |----------------------------+-----------------------------+----------------+
		'get_dump':        {'history':  True, 'bash':        'dump_get.sh', 'tag':  True, },
		'send_dump':       {'history':  True, 'bash':       'dump_send.sh', 'tag': False, },
		'del_dump':        {'history':  True, 'bash':        'dump_del.sh', 'tag': False, },
		# Backup |---------------------------+-----------------------------+----------------+
		'backup_db':       {'history':  True, 'bash':       'backup_db.sh', 'tag':  True, },
		'backup_sys':      {'history':  True, 'bash':      'backup_sys.sh', 'tag':  True, },
		'backup_full':     {'history':  True, 'bash':     'backup_full.sh', 'tag':  True, },
		# Main |-----------------------------+-----------------------------+----------------+
		'copy':            {'history':  True, 'bash':            'copy.sh', 'tag': False, },
		'script':          {'history':  True, 'bash':     'script_bash.sh', 'tag': False, },
		'update':          {'history':  True, 'bash':          'update.sh', 'tag':  True, },
		'copy_utils':      {'history':  True, 'bash':      'copy_utils.sh', 'tag': False, },
		'sql_script':      {'history':  True, 'bash':      'script_sql.sh', 'tag': False, }, }

	cmd = ''.join(selected['command'])
	selected['cmdname'] = dick[cmd]['bash']
	selected['history'] = dick[cmd]['history']
	return dick[cmd]['tag'], selected['history']


def run_date():
	"""Если не указана дата, возвращает текущую дату + 1 минута."""
	date = datetime.datetime.now() + datetime.timedelta(minutes=1)
	return date.strftime("%d.%m.%Y %H:%M")


def cmd_run(request, current_project, context):
	"""Запускает выбранную команду."""
	check_perm('run_command', current_project, request.user)

	selected = {
		'key':     get_key(),
		'user':    request.user,
		'date':    request.GET.get('selected_date') or run_date(),
		'rtype':   request.GET.get('run_type'),
		'dumps':   request.GET.getlist('selected_dumps'),
		'updates': request.GET.getlist('selected_updates'),
		'scripts': request.GET.getlist('selected_scripts'),
		'servers': request.GET.getlist('selected_servers'),
		'cronjbs': request.GET.getlist('selected_jobs'),
		'command': request.GET.get('selected_command'),
		'project': current_project, }

	con = {
		'date':  selected['date'].replace(' ', 'SS').replace(':', 'PP').replace('.', 'OO'),
		'cmd':   selected['command'],
		'rtype': selected['rtype'],
		'key':   selected['key'],
		'log':   'true', }

	context.update(con)
	command(selected)
	starter(selected)
	return context
