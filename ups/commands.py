# -*- encoding: utf-8 -*-

from .commands_engine import get_key
from .commands_engine import starter
from .permissions import check_perm
import datetime


def command(selected):
	"""Определяет команду(bash script) по полученному command id."""
# -----------------------+-------------------+-----------------------------+-----------------+----------------
#     -------------------|  Write history    |  Bash command name          |  Html tags in   |------------
	dick = {  # ---------|  log or not       |                             |  output         |--------
		# RUN only |-----+-------------------+-----------------------------+-----------------+---
		'delete_job':      {'history':  True, 'bash':      'delete_job.sh', 'tag': False, },
		'check_logs':      {'history': False, 'bash':      'check_logs.sh', 'tag': False, },
		'check_conf':      {'history': False, 'bash':      'check_conf.sh', 'tag': False, },
		'check_updates':   {'history': False, 'bash':   'check_updates.sh', 'tag': False, },
		# Maintenance |----------------------+-----------------------------+-----------------+
		'stop':            {'history':  True, 'bash':            'stop.sh', 'tag': False, },
		'start':           {'history':  True, 'bash':           'start.sh', 'tag': False, },
		'reload':          {'history':  True, 'bash':          'reload.sh', 'tag': False, },
		'restart':         {'history':  True, 'bash':         'restart.sh', 'tag': False, },
		'maintenance_on':  {'history':  True, 'bash':  'maintenance_on.sh', 'tag': False, },
		'maintenance_off': {'history':  True, 'bash': 'maintenance_off.sh', 'tag': False, },
		# Delete updates |-------------------+-----------------------------+-----------------+
		'del_all_updates': {'history':  True, 'bash': 'del_all_updates.sh', 'tag': False, },
		'del_sel_updates': {'history':  True, 'bash': 'del_sel_updates.sh', 'tag': False, },
		# Backup |---------------------------+-----------------------------+-----------------+
		'backup_db':       {'history':  True, 'bash':       'backup_db.sh', 'tag': False, },
		'backup_sys':      {'history':  True, 'bash':      'backup_sys.sh', 'tag': False, },
		'backup_full':     {'history':  True, 'bash':     'backup_full.sh', 'tag': False, },
		# Main |-----------------------------+-----------------------------+-----------------+
		'copy':            {'history':  True, 'bash':            'copy.sh', 'tag': False, },
		'script':          {'history':  True, 'bash':          'script.sh', 'tag': False, },
		'update':          {'history':  True, 'bash':          'update.sh', 'tag': False, },
		'get_dump':        {'history':  True, 'bash':        'get_dump.sh', 'tag':  True, },
		'copy_utils':      {'history':  True, 'bash':      'copy_utils.sh', 'tag': False, },
		'sql_script':      {'history':  True, 'bash':      'sql_script.sh', 'tag': False, }, }

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
		'key':  get_key(),
		'user': request.user,
		'cron': request.POST.get('CRON') or False,
		'date': request.POST.get('selected_date') or run_date(),
		'updates': request.POST.getlist('selected_updates'),
		'servers': request.POST.getlist('selected_servers'),
		'cronjbs': request.POST.getlist('selected_jobs'),
		'command': request.POST.get('selected_commands'),
		'project': current_project, }

	con = {
		'date': selected['date'].replace(' ', 'SS').replace(':', 'PP').replace('.', 'OO'),
		'cmd':  selected['command'],
		'cron': selected['cron'],
		'key':  selected['key'],
		'log':  'true', }

	context.update(con)
	command(selected)
	starter(selected)
	return context
