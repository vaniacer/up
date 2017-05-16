# -*- encoding: utf-8 -*-

from .commands_engine import get_key
from .commands_engine import starter
from .permissions import check_perm
import datetime


def command(selected):
	"""Определяет команду(bash script) по полученному command id."""
# ------------------------+------------------+-----------------------------+----------------+
# ------------------------+  write history   |  bash command name          |  html tags in  |
# ------------------------+  log or not      |                             |  output        |
	dick = {  # ----------+------------------+-----------------------------+----------------+
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
		'Maintenance_OFF': {'history':  True, 'bash': 'maintenance_off.sh', 'tag': False, }, }

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
