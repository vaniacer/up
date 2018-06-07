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
		'title': 'Cancel selected cron job(s).',  # Pop up help message
		'bash': 'cronjob_cancel.sh',              # Bash script that this command will start
		'name': 'cancel_job',                     # Web command name id(Internal command name id)
		'menu': 'Cancel job',                     # Menu name of the command
		'srv': 'false',                           # Check if some servers selected
		'upd': 'false',                           # Check if some updates selected
		'job': 'true',                            # Check if some cron jobs selected
		'scr': 'false',                           # Check if some scripts selected
		'dmp': 'false',                           # Check if some dumps selected
		'dgr': 'false',                           # If true will show confirmation window
		'run': "run_or_cron('RUN');",             # If set to "run_or_cron('RUN');" then command will be run only
		'history': True,                          # Save or not command log to history
		'tag':     False,                         # Show or not html tags in command log
		'cron':    True,                          # This command is for cronjobs
	},

	'change_date': {
		'position': 20,
		'name': 'change_date',
		'section': 'cron',
		'title': 'Change selected cron job(s) run date and time.',
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
		'history': True,
		'tag':     False,
		'cron':    True,
	},

	'permanent_job':   {
		'position': 30,
		'name': 'permanent_job',
		'section': 'cron',
		'title': 'Make selected cron job(s) permanent.',
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
		'history': True,
		'tag':     False,
		'cron':    True,
	},

	'once_job': {
		'position': 40,
		'name': 'once_job',
		'section': 'cron',
		'title': 'Make selected cron job(s) run once (default).',
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
		'history': True,
		'tag':     False,
		'cron':    True,
	},

	# Dumps section }---------------------------------------------------------------------------------------------------
	'get_dump': {
		'name': 'get_dump',
		'position': 10,
		'section': 'dump',
		'title': 'Get DB dump from selected server(s).',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	'del_dump': {
		'name': 'del_dump',
		'position': 20,
		'section': 'dump',
		'title': 'Delete selected dump(s) from UpS.',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'send_dump': {
		'name': 'send_dump',
		'position': 30,
		'section': 'dump',
		'title': "Recreate selected server's DB with this dump.",
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	# Updates section }-------------------------------------------------------------------------------------------------
	'copy': {
		'name': 'copy',
		'position': 10,
		'section': 'update',
		'title': 'Copy selected update(s) to selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'check_updates': {
		'name': 'check_updates',
		'position': 20,
		'section': 'update',
		'title': 'Check updates on selected server(s).',
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
		'history': False,
		'tag':     False,
		'cron':    False,
	},

	'update': {
		'name': 'update',
		'position': 30,
		'section': 'update',
		'title': 'Update selected server(s) with selected update file.',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	'del_sel_updates': {
		'name': 'del_sel_updates',
		'position': 40,
		'section': 'update',
		'title': 'Delete selected update(s) from selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'del_all_updates': {
		'name': 'del_all_updates',
		'position': 50,
		'section': 'update',
		'title': 'Delete all updates from selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	# Script section }--------------------------------------------------------------------------------------------------
	'run_script': {
		'name': 'run_script',
		'position': 10,
		'section': 'script',
		'title': 'Run selected script(s) on selected server(s).',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	# Server section }--------------------------------------------------------------------------------------------------

	# Maintenance
	'maintenance_on': {
		'name': 'maintenance_on',
		'position': 10,
		'section': 'server',
		'title': 'Show "Maintenance" page on selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'maintenance_off': {
		'name': 'maintenance_off',
		'position': 11,
		'section': 'server',
		'title': 'Hide "Maintenance" page on selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	# Jboss
	'reload': {
		'name': 'reload',
		'position': 20,
		'section': 'server',
		'title': 'Reload jboss config on selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'restart': {
		'name': 'restart',
		'position': 21,
		'section': 'server',
		'title': 'Restart jboss on selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'start': {
		'name': 'start',
		'position': 22,
		'section': 'server',
		'title': 'Start jboss(krupd jboss.start) on selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'stop': {
		'name': 'stop',
		'section': 'server',
		'position': 23,
		'title': 'Stop jboss(krupd jboss.stop) on selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'kill': {
		'name': 'kill',
		'position': 24,
		'section': 'server',
		'title': 'Kill jboss(krupd jboss.kill) on selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
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
		'history': False,
		'tag':     True,
		'cron':    False,
	},

	'check_conf': {
		'name': 'check_conf',
		'position': 40,
		'section': 'server',
		'title': 'Show conf(standalone-full.xml) and java options of selected server(s).',
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
		'history': False,
		'tag':     False,
		'cron':    False,
	},

	# Logs
	'check_logs': {
		'name': 'check_logs',
		'position': 50,
		'section': 'server',
		'title': 'Check logs on selected server(s).',
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
		'history': False,
		'tag':     False,
		'cron':    False,
	},


	'get_logs_day': {
		'name': 'get_logs_day',
		'position': 51,
		'section': 'server',
		'title': 'Get day logs from selected server(s).',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	'get_logs_all': {
		'name': 'get_logs_all',
		'position': 52,
		'section': 'server',
		'title': 'Get all logs from selected server(s).',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	# Backup
	'backup_db': {
		'name': 'backup_db',
		'position': 60,
		'section': 'server',
		'title': 'Database backup via "./krupd bkp db". \
Files will be stored on the server(s) and downloaded to UpS.',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	'backup_sys': {
		'name': 'backup_sys',
		'position': 61,
		'section': 'server',
		'title': 'System backup via "./krupd bkp sys". \
Files will be stored on the server(s) and downloaded to UpS.',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	'backup_full': {
		'name': 'backup_full',
		'position': 62,
		'section': 'server',
		'title': 'System and DB backup via "./krupd bkp full". \
Files will be stored on the server(s) and downloaded to UpS.',
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
		'history': True,
		'tag':     True,
		'cron':    False,
	},

	'copy_utils': {
		'name': 'copy_utils',
		'position': 70,
		'section': 'server',
		'title': 'Copy utils folder to selected server(s).',
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
		'history': True,
		'tag':     False,
		'cron':    False,
	},

	'tunnel': {
		'name': 'tunnel',
		'position': 80,
		'section': 'server',
		'title': 'Make ssh tunnel to the bind port of selected server(s).',
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
		'history': False,
		'tag':     True,
		'cron':    False,
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


def job_opt(selected, job):
	"""В зависимости от выбранного действия с кронжобом, удаляет либо меняет job.perm статус."""
	if selected['command'] == 'permanent_job':
		job.cdat = 'Everyday %s' % job.cdat.split()[-1]
		job.perm = True
		job.save()
	if selected['command'] == 'change_date':
		job.cdat = selected['date']
		job.save()
	if selected['command'] == 'cancel_job':
		job.delete()
	if selected['command'] == 'once_job':
		job.cdat = '%s %s' % (datetime.datetime.now().strftime("%Y-%m-%d"), job.cdat.split()[-1])
		job.perm = False
		job.save()


def add_event(selected, log, err, cron, uniq, date, serv):
	"""Создает событие в истории."""
	History.objects.create(
		name=selected['name'].capitalize().replace('_', ' '),
		proj=selected['project'],
		user=selected['user'],
		serv=serv,
		cron=cron,
		uniq=uniq,
		cdat=date,
		desc=log,
		exit=err,
	)


def add_job(selected, log, cron, serv):
	"""Создает запись о крон жобе."""
	Job.objects.create(
		name=selected['command'].capitalize().replace('_', ' '),
		proj=selected['project'],
		user=selected['user'],
		cdat=selected['date'],
		perm=False,
		serv=serv,
		cron=cron,
		desc=log,
	)


def starter(selected):
	"""Выполняет комманду."""
	opt = [
		conf.BASE_DIR + '/bash/starter.sh',
		'-prj',  '%s:%s' % (str(selected['project'].id), str(selected['project'].name)),
		'-date', selected['date'],
		'-key',  selected['key']
	]

	opt.extend(selected['opt'])

	for ID in selected['updates']:
		update = get_object_or_404(Update, id=ID)
		opt.extend(['-u', str(update.file)])

	for ID in selected['scripts']:
		script = get_object_or_404(Script, id=ID)
		opt.extend(['-x', str(script.file)])

	for dump in selected['dumps']:
		opt.extend(['-m', str(dump)])

	if conf.DEBUG:
		print '\n', opt, '\n\n', selected, '\n'

	Popen(opt)


def cmd_run(data, project, user):
	"""Запускает выбранную команду."""
	check_perm_or404('run_command', project, user)

	crn = ''
	logid = ''
	date = run_date()
	cmd = data['selected_command']

	job = commandick[cmd]['cron']
	his = commandick[cmd]['history']

	if data['selected_date'] and data['selected_time']:
		date = '%s %s' % (data['selected_date'], data['selected_time'])

	selected = {
		'name':    cmd,
		'command': cmd,
		'date':    date,
		'user':    user,
		'project': project,
		'rtype':   data['run_type'],
		'bashcmd': commandick[cmd]['bash'],
		'dumps':   data.getlist('selected_dumps'),
		'updates': data.getlist('selected_updates'),
		'scripts': data.getlist('selected_scripts'),
	}

	if job:
		for job_id in data.getlist('selected_jobs'):
			jobobj = get_object_or_404(Job, cron=job_id)
			server = jobobj.serv
			key = get_key()
			selected['key'] = key
			logid = logid + '&logid=%s' % key
			selected['opt'] = ['-job', job_id, '-hid', key, '-cmd', selected['bashcmd']]
			add_event(selected, 'Working...', '', key, key, date, server)

			job_opt(selected, jobobj)
			starter(selected)
	else:
		for server_id in data.getlist('selected_servers'):

			key = get_key()
			selected['key'] = key
			logid = logid + '&logid=%s' % key
			server = get_object_or_404(Server, id=server_id)
			selected['opt'] = ['-server', '%s:%s:%s' % (server.addr, server.wdir, server.port), ]

			if data['run_type'] == 'CRON':
				if not his:
					return '/projects/%s/?%s' % (project.id, info(data))
				crn = key
				add_job(selected, 'Working...', key, server)
				selected['name'] = 'Set cron job - %s' % selected['command'].lower()
				selected['opt'].extend(['-cmd',  'cron.sh', '-run',  selected['bashcmd'], '-cid', key, ])
			else:
				selected['opt'].extend(['-cmd', selected['bashcmd']])

			if his:
				selected['opt'].extend(['-hid', key])
				add_event(selected, 'Working...', '', crn, key, date, server)

			starter(selected)

	if his:
		url = '/projects/%s/?cmdlog=%s%s%s' % (project.id, selected['command'], info(data), logid,)
	else:
		url = '/command_log/?cmd=%s&prid=%s%s%s' % (selected['command'], project.id, info(data), logid,)

	return url
