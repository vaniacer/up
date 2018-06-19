# -*- encoding: utf-8 -*-

from .models import Server, History, Job, Update, Script
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .permissions import check_perm_or404
from django.conf import settings as conf
from subprocess import Popen
from base64 import b64encode
from os import urandom
import datetime


commandick = {

	# Cron submenu }----------------------------------------------------------------------------------------------------
	'cancel_job': {                               # Internal command name id
		'position': 10,                           # Position in commands list(dick sorted by position)
		'section': 'cron',                        # Section in which command will be placed
		'class': '',                              # Class assigned to a command button(for example 'danger')
		'title': 'Cancel dick cron job(s).',  # Pop up help message
		'bash': 'cronjob_cancel.sh',              # Bash script that this command will start
		'name': 'cancel_job',                     # Web command name id(Internal command name id)
		'menu': 'Cancel job',                     # Menu name of the command
		'srv': 'false',                           # Check if some servers dick
		'upd': 'false',                           # Check if some updates dick
		'job': 'true',                            # Check if some cron jobs dick
		'scr': 'false',                           # Check if some scripts dick
		'dmp': 'false',                           # Check if some dumps dick
		'dgr': 'false',                           # If true will show confirmation window
		'run': "run_or_cron('RUN');",             # If set to "run_or_cron('RUN');" then command will be run only
		'his': True,                              # Save or not command log to history
		'tag': False,                             # Show or not html tags in command log
	},

	'change_date': {
		'position': 20,
		'name': 'change_date',
		'section': 'cron',
		'title': 'Change dick cron job(s) run date and time.',
		'class': '',
		'menu': 'Change date',
		'bash': 'cronjob_date.sh',
		'srv': 'false',
		'upd': 'false',
		'job': 'true',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': True,
		'tag': False,
	},

	'permanent_job':   {
		'position': 30,
		'name': 'permanent_job',
		'section': 'cron',
		'title': 'Make dick cron job(s) permanent.',
		'class': '',
		'menu': 'Run everyday',
		'bash': 'cronjob_perm.sh',
		'srv': 'false',
		'upd': 'false',
		'job': 'true',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': True,
		'tag': False,
	},

	'once_job': {
		'position': 40,
		'name': 'once_job',
		'section': 'cron',
		'title': 'Make dick cron job(s) run once (default).',
		'class': '',
		'menu': 'Run once',
		'bash': 'cronjob_once.sh',
		'srv': 'false',
		'upd': 'false',
		'job': 'true',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': True,
		'tag': False,
	},

	# Dumps section }---------------------------------------------------------------------------------------------------
	'get_dump': {
		'name': 'get_dump',
		'position': 10,
		'section': 'dump',
		'title': 'Get DB dump from dick server(s).',
		'class': '',
		'menu': 'Get dump',
		'bash': 'dump_get.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': True,
	},

	'del_dump': {
		'name': 'del_dump',
		'position': 20,
		'section': 'dump',
		'title': 'Delete dick dump(s) from UpS.',
		'class': '',
		'menu': 'Del dump',
		'bash': 'dump_del.sh',
		'srv': 'false',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'true',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': False,
	},

	'send_dump': {
		'name': 'send_dump',
		'position': 30,
		'section': 'dump',
		'title': "Recreate dick server's DB with this dump.",
		'class': 'danger',
		'menu': 'Send dump',
		'bash': 'dump_send.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'true',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': True,
	},

	# Updates section }-------------------------------------------------------------------------------------------------
	'copy': {
		'name': 'copy',
		'position': 10,
		'section': 'update',
		'title': 'Copy dick update(s) to dick server(s).',
		'class': '',
		'menu': 'Copy',
		'bash': 'copy.sh',
		'srv': 'true',
		'upd': 'true',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': False,
	},

	'check_updates': {
		'name': 'check_updates',
		'position': 20,
		'section': 'update',
		'title': 'Check updates on dick server(s).',
		'class': '',
		'menu': 'Check',
		'bash': 'check_updates.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': False,
		'tag': False,
	},

	'update': {
		'name': 'update',
		'position': 30,
		'section': 'update',
		'title': 'Update dick server(s) with dick update file.',
		'class': 'danger',
		'menu': 'Start Update',
		'bash': 'update.sh',
		'srv': 'true',
		'upd': 'true',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': True,
	},

	'del_sel_updates': {
		'name': 'del_sel_updates',
		'position': 40,
		'section': 'update',
		'title': 'Delete dick update(s) from dick server(s).',
		'class': '',
		'menu': 'Delete updates',
		'bash': 'del_sel_updates.sh',
		'srv': 'true',
		'upd': 'true',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': False,
	},

	'del_all_updates': {
		'name': 'del_all_updates',
		'position': 50,
		'section': 'update',
		'title': 'Delete all updates from dick server(s).',
		'class': '',
		'menu': 'Delete all updates',
		'bash': 'del_all_updates.sh',
		'srv': 'true',
		'upd': 'true',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': False,
	},

	# Script section }--------------------------------------------------------------------------------------------------
	'run_script': {
		'name': 'run_script',
		'position': 10,
		'section': 'script',
		'title': 'Run dick script(s) on dick server(s).',
		'class': '',
		'menu': 'Run script(s)',
		'bash': 'run_script.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'true',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': True,
	},

	# Server section }--------------------------------------------------------------------------------------------------

	# Maintenance
	'maintenance_on': {
		'name': 'maintenance_on',
		'position': 10,
		'section': 'server',
		'title': 'Show "Maintenance" page on dick server(s).',
		'class': 'danger',
		'menu': 'Maintenance ON',
		'bash': 'maintenance_on.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': False,
	},

	'maintenance_off': {
		'name': 'maintenance_off',
		'position': 11,
		'section': 'server',
		'title': 'Hide "Maintenance" page on dick server(s).',
		'class': 'danger',
		'menu': 'Maintenance Off',
		'bash': 'maintenance_off.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': False,
	},

	# Jboss
	'reload': {
		'name': 'reload',
		'position': 20,
		'section': 'server',
		'title': 'Reload jboss config on dick server(s).',
		'class': 'danger',
		'menu': 'Reload config',
		'bash': 'jboss_reload.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': False,
	},

	'restart': {
		'name': 'restart',
		'position': 21,
		'section': 'server',
		'title': 'Restart jboss on dick server(s).',
		'class': 'danger',
		'menu': 'Restart jboss',
		'bash': 'jboss_restart.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': False,
	},

	'start': {
		'name': 'start',
		'position': 22,
		'section': 'server',
		'title': 'Start jboss(krupd jboss.start) on dick server(s).',
		'class': 'danger',
		'menu': 'Start jboss',
		'bash': 'jboss_start.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': False,
	},

	'stop': {
		'name': 'stop',
		'section': 'server',
		'position': 23,
		'title': 'Stop jboss(krupd jboss.stop) on dick server(s).',
		'class': 'danger',
		'menu': 'Stop jboss',
		'bash': 'jboss_stop.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': False,
	},

	'kill': {
		'name': 'kill',
		'position': 24,
		'section': 'server',
		'title': 'Kill jboss(krupd jboss.kill) on dick server(s).',
		'class': 'danger',
		'menu': 'Kill jboss',
		'bash': 'jboss_kill.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'his': True,
		'tag': False,
	},

	'server_info': {
		'name': 'server_info',
		'position': 30,
		'section': 'server',
		'title': 'Show system info: CPU, mem, disk etc.',
		'class': '',
		'menu': 'System Info',
		'bash': 'server_info.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': False,
		'tag': True,
	},

	'check_conf': {
		'name': 'check_conf',
		'position': 40,
		'section': 'server',
		'title': 'Show conf(standalone-full.xml) and java options of dick server(s).',
		'class': '',
		'menu': 'Check conf',
		'bash': 'check_conf.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': False,
		'tag': False,
	},

	# Logs
	'check_logs': {
		'name': 'check_logs',
		'position': 50,
		'section': 'server',
		'title': 'Check logs on dick server(s).',
		'class': '',
		'menu': 'Check logs',
		'bash': 'check_logs.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': False,
		'tag': False,
	},


	'get_logs_day': {
		'name': 'get_logs_day',
		'position': 51,
		'section': 'server',
		'title': 'Get day logs from dick server(s).',
		'class': '',
		'menu': 'Get day logs',
		'bash': 'logs_get_day.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': True,
	},

	'get_logs_all': {
		'name': 'get_logs_all',
		'position': 52,
		'section': 'server',
		'title': 'Get all logs from dick server(s).',
		'class': '',
		'menu': 'Get all logs',
		'bash': 'logs_get_all.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': True,
	},

	# Backup
	'backup_db': {
		'name': 'backup_db',
		'position': 60,
		'section': 'server',
		'title': 'Database backup, files will be stored on the server(s) and downloaded to UpS.',
		'class': '',
		'menu': 'Backup base',
		'bash': 'backup_db.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': True,
	},

	'backup_sys': {
		'name': 'backup_sys',
		'position': 61,
		'section': 'server',
		'title': 'System backup files will be stored on the server(s) and downloaded to UpS.',
		'class': '',
		'menu': 'Backup system',
		'bash': 'backup_sys.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': True,
	},

	'backup_full': {
		'name': 'backup_full',
		'position': 62,
		'section': 'server',
		'title': 'System and DB backup files will be stored on the server(s) and downloaded to UpS.',
		'class': '',
		'menu': 'Backup full',
		'bash': 'backup_full.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': True,
	},

	'copy_utils': {
		'name': 'copy_utils',
		'position': 70,
		'section': 'server',
		'title': 'Copy utils folder to dick server(s).',
		'class': '',
		'menu': 'Copy utils',
		'bash': 'copy_utils.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'his': True,
		'tag': False,
	},

	'tunnel': {
		'name': 'tunnel',
		'position': 80,
		'section': 'server',
		'title': 'Make ssh tunnel to the bind port of dick server(s).',
		'class': '',
		'menu': 'Create tunnel',
		'bash': 'tunnel.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'false',
		'run': "run_or_cron('RUN');",
		'his': False,
		'tag': True,
	},
}


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
	if data.get('scripts'):
		url += '&scripts=%s' % data.get('scripts')
	if data.get('updates'):
		url += '&updates=%s' % data.get('updates')
	if data.get('dumps'):
		url += '&dumps=%s' % data.get('dumps')
	if data.get('tab'):
		url += '&tab=%s' % data.get('tab')
	return url


def get_key():
	"""Создает случайную последовательность символов."""
	return str(b64encode(urandom(6), 'dfsDFAsfsf'))


def run_date():
	"""Если не указана дата, возвращает текущую дату + 1 минута."""
	date = datetime.datetime.now() + datetime.timedelta(minutes=1)
	return date.strftime("%Y-%m-%d %H:%M")


def del_job(job_id):
	"""Удаляет из базы запись о крон жобе."""
	try:
		get_object_or_404(Job, cron=job_id).delete()
	except ObjectDoesNotExist:
		pass


def add_job(dick):
	"""Создает запись о крон жобе."""
	Job.objects.create(
		name=dick['name'].capitalize().replace('_', ' '),
		proj=dick['proj'],
		user=dick['user'],
		cdat=dick['cdat'],
		serv=dick['serv'],
		cron=dick['cron'],
		desc=dick['desc'],
	)


def add_event(dick):
	"""Создает событие в истории."""
	History.objects.create(
		name=dick['name'].capitalize().replace('_', ' '),
		proj=dick['proj'],
		user=dick['user'],
		serv=dick['serv'],
		cron=dick['cron'],
		uniq=dick['uniq'],
		cdat=dick['cdat'],
		desc=dick['desc'],
		exit=dick['exit'],
	)


def job_opt(dick):
	"""В зависимости от выбранного действия с кронжобой, удаляет либо меняет job.perm статус."""
	if dick['name'] == 'permanent_job':
		dick['jobj'].cdat = 'Everyday %s' % dick['jobj'].cdat.split()[-1]
		dick['jobj'].perm = True
		dick['jobj'].save()

	if dick['name'] == 'change_date':
		dick['jobj'].cdat = dick['cdat']
		dick['jobj'].save()

	if dick['name'] == 'cancel_job':
		dick['jobj'].delete()

	if dick['name'] == 'once_job':
		dick['jobj'].cdat = '%s %s' % (
			datetime.datetime.now().strftime("%Y-%m-%d"),
			dick['jobj'].cdat.split()[-1]
		)
		dick['jobj'].perm = False
		dick['jobj'].save()


def history(dick):
	"""Создает событие в истории"""
	if dick['his']:
		dick['opt'].extend(['-hid', dick['uniq']])
		add_event(dick)


def starter(dick):
	"""Выполняет комманду."""

	history(dick)

	opt = [
		conf.BASE_DIR + '/bash/starter.sh',
		'-prj',  '%s:%s' % (str(dick['proj'].id), str(dick['proj'].name)),
		'-date', dick['cdat'],
		'-key',  dick['uniq']
	]

	opt.extend(dick['opt'])

	for ID in dick['data'].getlist('selected_updates'):
		update = get_object_or_404(Update, id=ID)
		opt.extend(['-u', str(update.file)])

	for ID in dick['data'].getlist('selected_scripts'):
		script = get_object_or_404(Script, id=ID)
		opt.extend(['-x', str(script.file)])
		if dick['data'].get('script_opt' + ID):
			opt.extend(['-o', dick['data'].get('script_opt' + ID)])

	for dump in dick['data'].getlist('selected_dbdumps'):
		opt.extend(['-m', str(dump)])

	if conf.DEBUG:
		print '\n', opt, '\n\n', dick, '\n'

	Popen(opt)


def run_cmd(data, project, user):
	"""Запускает выбранную команду."""
	check_perm_or404('run_command', project, user)

	date = run_date()

	name = data['selected_command']
	bash = commandick[name]['bash']

	if data['selected_date'] and data['selected_time']:
		date = '%s %s' % (data['selected_date'], data['selected_time'])

	dick = {
		'jobj': '',
		'cron': '',
		'uniq': '',
		'exit': '',
		'logi': '',
		'serv': None,
		'name': name,
		'user': user,
		'cdat': date,
		'data': data,
		'proj': project,
		'desc': 'Working...',

		'his': commandick[name]['his'],
		'job': commandick[name]['job'],
		'srv': commandick[name]['srv'],
	}

	# Cronjob specific commands
	if dick['job'] == 'true':

		for jobi in data.getlist('selected_jobs'):

			jobj = get_object_or_404(Job, cron=jobi)
			serv = jobj.serv
			uniq = get_key()

			dick['logi'] += '&logid=%s' % uniq
			dick['opt'] = ['-job', jobi, '-cmd', bash]
			dick.update({'cron': uniq, 'uniq': uniq, 'serv': serv, 'jobj': jobj})

			job_opt(dick)
			starter(dick)

	# Commands that can run without server(s)
	elif dick['srv'] == 'false':

			uniq = get_key()

			dick.update({'uniq': uniq})
			dick['opt'] = ['-cmd', bash]
			dick['logi'] += '&logid=%s' % uniq

			starter(dick)

	# Server commands
	else:

		for server_id in data.getlist('selected_servers'):

			uniq = get_key()
			serv = get_object_or_404(Server, id=server_id)

			dick['logi'] += '&logid=%s' % uniq
			dick.update({'uniq': uniq, 'serv': serv})
			dick['opt'] = ['-server', '%s:%s:%s' % (serv.addr, serv.wdir, serv.port)]

			if data['run_type'] == 'CRON':
				if not dick['his']:
					return '/projects/%s/?%s' % (project.id, info(data))

				dick.update({'cron': uniq, 'cdat': date})
				add_job(dick)

				dick['name'] = 'Set cron job - %s' % name.lower()
				dick['opt'].extend(['-cmd',  'cron.sh', '-run', bash, '-cid', uniq])
			else:
				dick['opt'].extend(['-cmd', bash])

			starter(dick)

	if dick['his']:
		url = '/projects/%s/?cmdlog=%s%s%s' % (project.id, name, info(data), dick['logi'])
	else:
		url = '/command_log/?cmd=%s&prid=%s%s%s' % (name, project.id, info(data), dick['logi'])

	return url
