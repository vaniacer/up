# -*- encoding: utf-8 -*-

from .models import Server, History, Job, Update, Script
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .permissions import check_perm_or404
from django.conf import settings as conf
from datetime import datetime, timedelta
from os.path import join as opj
from subprocess import Popen
from base64 import b64encode
from re import split, escape
from os import urandom


class CommandClass:
	"""Класс команды"""
	def __init__(
		self,
		permission='',  # Permission needed to run this command.
		position=1,     # Position in commands list
		section='',     # Section command will be placed to(scripts, updates, dumps, cron, servers)
		style='',       # Class assigned to a command button(for example 'danger')
		title='',       # Pop up help message(via title)
		menu='',        # Command name in UI
		name='',        # Command name(an internal command name)
		run='',         # Pre validation command, if set to "run_or_cron('RUN');" then command will be run only
		his=True,       # If True, command log will be saved to history
		dgr='false',    # If true will show confirmation window
		job='false',    # Check if some cron jobs selected
		srv='false',    # Check if some servers selected
		upd='false',    # Check if some updates selected
		scr='false',    # Check if some scripts selected
		dmp='false',    # Check if some dumps selected
	):
		self.permission = permission
		self.position = position
		self.section = section
		self.style = style
		self.title = title
		self.name = name
		self.menu = menu
		self.srv = srv
		self.upd = upd
		self.job = job
		self.scr = scr
		self.dmp = dmp
		self.dgr = dgr
		self.run = run
		self.his = his


commandick = {

	# Cron submenu }----------------------------------------------------------------------------------------------------
	'cancel_job': CommandClass(
		permission='run_cron',
		position=4,
		section='cron',
		title='Cancel selected cron job(s).',
		name='cancel_job',
		menu='Remove job(s)',
		job='true',
		run="run_or_cron('RUN');",
	),

	'permanent_job': CommandClass(
		permission='run_cron',
		position=3,
		section='cron',
		title='Make selected cron job(s) permanent.',
		name='permanent_job',
		menu='Run everyday',
		job='true',
		run="run_or_cron('RUN');",
	),

	'once_job': CommandClass(
		permission='run_cron',
		position=2,
		section='cron',
		title='Make selected cron job(s) run once (default).',
		name='once_job',
		menu='Run one time',
		job='true',
		run="run_or_cron('RUN');",
	),

	'change_date': CommandClass(
		permission='run_cron',
		position=1,
		section='cron',
		title='Change selected cron job(s) run date and time. If date\\time not set, it will set current date\\time.',
		name='change_date',
		menu='Change date',
		job='true',
		run="run_or_cron('RUN');",
	),

	# Dumps section }---------------------------------------------------------------------------------------------------
	'get_dump': CommandClass(
		section='dump',
		title='Get DB dump from selected server(s).',
		name='get_dump',
		menu='Get dump(s)',
		srv='true',
	),

	'del_dump': CommandClass(
		permission='del_dump',
		position=20,
		section='dump',
		title='Delete selected dump(s) from UpS.',
		name='del_dump',
		menu='Del dump(s)',
		dmp='true',
	),

	'send_dump': CommandClass(
		permission='send_dump',
		position=30,
		section='dump',
		style='danger',
		title="Recreate selected server's DB with this dump.",
		name='send_dump',
		menu='Send dump',
		srv='true',
		dgr='true',
	),

	# Updates section }-------------------------------------------------------------------------------------------------
	'copy': CommandClass(
		permission='run_update',
		section='update',
		title='Copy selected update(s) to selected server(s).',
		name='copy',
		menu='Copy update(s)',
		srv='true',
	),

	'check_updates': CommandClass(
		permission='run_update',
		position=20,
		section='update',
		title='Check updates on selected server(s).',
		name='check_updates',
		menu='Check updates',
		srv='true',
		run="run_or_cron('RUN');",
		his=False,
	),

	'update': CommandClass(
		permission='run_update',
		position=30,
		section='update',
		style='danger',
		title='Update selected server(s) with selected update file.',
		name='update',
		menu='Start Update',
		srv='true',
		upd='true',
		dgr='true',
	),

	'del_sel_updates': CommandClass(
		permission='run_update',
		position=40,
		section='update',
		title='Delete selected update(s) from selected server(s).',
		name='del_sel_updates',
		menu='Delete update(s)',
		srv='true',
		upd='true',
	),

	'del_all_updates': CommandClass(
		permission='run_update',
		position=50,
		section='update',
		title='Delete all updates from selected server(s).',
		name='del_all_updates',
		menu='Delete all updates',
		srv='true',
	),

	# Script section }--------------------------------------------------------------------------------------------------
	'run_script': CommandClass(
		permission='run_script',
		section='script',
		title='Run selected script(s) on selected server(s).',
		name='run_script',
		menu='Run script(s)',
		srv='true',
		scr='true',
	),

	# Server section }--------------------------------------------------------------------------------------------------

	# Maintenance
	'maintenance_on': CommandClass(
		permission='maintenance',
		section='server',
		style='danger',
		title='Show "Maintenance" page on selected server(s).',
		name='maintenance_on',
		menu='Maintenance ON',
		srv='true',
		dgr='true',
	),

	'maintenance_off': CommandClass(
		permission='maintenance',
		position=11,
		section='server',
		style='danger',
		title='Hide "Maintenance" page on selected server(s).',
		name='maintenance_off',
		menu='Maintenance Off',
		srv='true',
		dgr='true',
	),

	# Jboss
	'reload': CommandClass(
		permission='maintenance',
		position=20,
		section='server',
		style='danger',
		title='Reload jboss config on selected server(s).',
		name='reload',
		menu='Reload config',
		srv='true',
		dgr='true',
	),

	'restart': CommandClass(
		permission='maintenance',
		position=21,
		section='server',
		style='danger',
		title='Restart jboss on selected server(s).',
		name='restart',
		menu='Restart jboss',
		srv='true',
		dgr='true',
	),

	'start': CommandClass(
		permission='maintenance',
		position=22,
		section='server',
		style='danger',
		title='Start jboss(krupd jboss.start) on selected server(s).',
		name='start',
		menu='Start jboss',
		srv='true',
		dgr='true',
	),

	'stop': CommandClass(
		permission='maintenance',
		position=23,
		section='server',
		style='danger',
		title='Stop jboss(krupd jboss.stop) on selected server(s).',
		name='stop',
		menu='Stop jboss',
		srv='true',
		dgr='true',
	),

	'kill': CommandClass(
		permission='maintenance',
		position=24,
		section='server',
		style='danger',
		title='Kill jboss(krupd jboss.kill) on selected server(s).',
		name='kill',
		menu='Kill jboss',
		srv='true',
		dgr='true',
	),

	# Info
	'server_info': CommandClass(
		position=30,
		section='server',
		title='Show system info: CPU, mem, disk etc.',
		name='server_info',
		menu='System Info',
		srv='true',
		run="run_or_cron('RUN');",
		his=False,
	),

	'check_conf': CommandClass(
		position=40,
		section='server',
		title='Show conf(standalone-full.xml) and java options of selected server(s).',
		name='check_conf',
		menu='Check conf',
		srv='true',
		run="run_or_cron('RUN');",
		his=False,
	),

	# Logs
	'check_logs': CommandClass(
		position=50,
		section='server',
		title='Check logs on selected server(s).',
		name='check_logs',
		menu='Check logs',
		srv='true',
		run="run_or_cron('RUN');",
		his=False,
	),

	'get_logs_day': CommandClass(
		position=51,
		section='server',
		title='Get day logs from selected server(s).',
		name='get_logs_day',
		menu='Get day logs',
		srv='true',
	),

	'get_logs_all': CommandClass(
		position=52,
		section='server',
		title='Get all logs from selected server(s).',
		name='get_logs_all',
		menu='Get all logs',
		srv='true',
	),

	# Backup
	'backup_db': CommandClass(
		permission='maintenance',
		position=60,
		section='server',
		title='Database backup, files will be stored on the server(s) and downloaded to UpS.',
		name='backup_db',
		menu='Backup base',
		srv='true',
	),

	'backup_sys': CommandClass(
		permission='maintenance',
		position=61,
		section='server',
		title='System backup files will be stored on the server(s) and downloaded to UpS.',
		name='backup_sys',
		menu='Backup system',
		srv='true',
	),

	'backup_full': CommandClass(
		permission='maintenance',
		position=62,
		section='server',
		title='System and DB backup files will be stored on the server(s) and downloaded to UpS.',
		name='backup_full',
		menu='Backup full',
		srv='true',
	),

	'copy_utils': CommandClass(
		permission='maintenance',
		position=70,
		section='server',
		title='Copy utils folder to selected server(s).',
		name='copy_utils',
		menu='Copy utils',
		srv='true',
	),

	'peep_pass': CommandClass(
		permission='peep_pass',
		position=75,
		section='server',
		title='Peep passwords from file krista-users.properties.',
		name='peep_pass',
		menu='Peep passwords',
		srv='true',
		run="run_or_cron('RUN');",
		his=False,
	),

	'tunnel': CommandClass(
		position=80,
		section='server',
		title='Make ssh tunnel to the bind port of selected server(s).',
		name='tunnel',
		menu='Create tunnel',
		srv='true',
		run="run_or_cron('RUN');",
		his=False,
	),
}


def info(data, tab=''):
	url = u''
	if data.get('server_info'):
		url += u'&server_info=on'
	if data.get('script_info'):
		url += u'&script_info=on'
	if data.get('update_info'):
		url += u'&update_info=on'
	if data.get('dbdump_info'):
		url += u'&dbdump_info=on'
	if data.get('job_info'):
		url += u'&job_info=on'
	if data.get('servers'):
		url += u'&servers=%s' % data.get('servers')
	if data.get('scripts'):
		url += u'&scripts=%s' % data.get('scripts')
	if data.get('updates'):
		url += u'&updates=%s' % data.get('updates')
	if data.get('dumps'):
		url += u'&dumps=%s' % data.get('dumps')
	if data.get('jobs'):
		url += u'&jobs=%s' % data.get('jobs')
	if tab:
		url += u'#%s' % tab
	elif data.get('tab'):
		url += u'#%s' % data.get('tab')
	return url


def back_url(data):
	"""Возвращает url проекта с тек. параметрами."""
	return u'/projects/{project_id!s}/?{parameters!s}'.format(
		project_id=data['prid'],
		parameters=info(data),
	)


def get_key():
	"""Создает случайную последовательность символов."""
	return str(b64encode(urandom(6), 'dfsDFAsfsf'))


def run_date():
	"""Если не указана дата, возвращает текущую дату + 1 минута."""
	date = datetime.now() + timedelta(minutes=1)
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
		name=dick['cmnd'].capitalize().replace('_', ' '),
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
			datetime.now().strftime("%Y-%m-%d"),
			dick['jobj'].cdat.split()[-1]
		)
		dick['jobj'].perm = False
		dick['jobj'].save()


def history(dick):
	"""Создает событие в истории"""
	if dick['his']:
		dick['opt'].extend(['--history'])
		add_event(dick)


def starter(dick):
	"""Выполняет комманду."""

	history(dick)
	python = opj(conf.BASE_DIR, '../env/bin/python')
	opt = [
		python, 'starter.py', dick['cmnd'],
		'--proname', str(dick['proj'].name),
		'--proid', str(dick['proj'].id),
		'--date', dick['cdat'],
		'--key', dick['uniq'],
	]

	opt.extend(dick['opt'])

	for ID in dick['data'].getlist('selected_updates'):
		update = get_object_or_404(Update, id=ID)
		opt.extend(['-u', str(update.file)])

	for ID in dick['data'].getlist('selected_scripts'):
		script = get_object_or_404(Script, id=ID)
		opt.extend(['-x', str(script.file)])
		# split options string coz re.escape escapes spaces as well
		oplist = split(' ', str(dick['data'].get('script_opt' + ID)))
		# join it back and escape special symbols
		opdone = ' '.join(escape(opt) for opt in oplist)
		# add result as script arg -o 'test 123'
		opt.extend(['-o', opdone])

	for dump in dick['data'].getlist('selected_dbdumps'):
		opt.extend(['-m', str(dump)])

	if conf.DEBUG:
		print '\n', opt, '\n\n', dick, '\n'

	Popen(opt)


def run_cmd(data, project, user):
	"""Запускает выбранную команду."""
	check_perm_or404('run_command', project, user)

	tab = ''
	date = run_date()
	name = data['run_cmnd']

	# Check command permission
	if commandick[name].permission:
		check_perm_or404(commandick[name].permission, project, user)

	if data.get('selected_date', default=None) and data.get('selected_time', default=None):
		date = '%s %s' % (data['selected_date'], data['selected_time'])

	dick = {
		'opt': [],
		'jobj': '',
		'cron': '',
		'uniq': '',
		'exit': '',
		'logi': '',
		'serv': None,
		'cmnd': name,
		'name': name,
		'user': user,
		'cdat': date,
		'data': data,
		'proj': project,
		'desc': 'Working...',

		'his':  commandick[name].his,
		'job':  commandick[name].job,
		'srv':  commandick[name].srv,
	}

	# Cronjob specific commands
	if dick['job'] == 'true':

		tab = 'cron'

		for jobi in data.getlist('selected_jobs'):

			jobj = get_object_or_404(Job, cron=jobi)
			serv = jobj.serv
			uniq = get_key()

			dick['opt'] = ['--job', jobi]
			dick['logi'] += '&logid=%s' % uniq
			dick.update({'cron': jobi, 'uniq': uniq, 'serv': serv, 'jobj': jobj})

			job_opt(dick)
			starter(dick)

	# Commands that can run without server(s)
	elif dick['srv'] == 'false':

			uniq = get_key()

			dick.update({'uniq': uniq})
			dick['logi'] += '&logid=%s' % uniq

			starter(dick)

	# Server commands
	else:

		tab = 'logs'

		for server_id in data.getlist('selected_servers'):

			uniq = get_key()
			serv = get_object_or_404(Server, id=server_id)

			dick['logi'] += '&logid=%s' % uniq
			dick.update({'uniq': uniq, 'serv': serv})
			dick['opt'] = ['--server', serv.addr, '--wdir', serv.wdir, '--port', serv.port]

			if data['run_type'] == 'CRON':
				if not dick['his']:
					return back_url(data)

				dick.update({'cron': uniq, 'cdat': date})
				add_job(dick)

				dick['name'] = 'Set cron job - %s' % name.lower()
				dick['opt'].extend(['--cron'])

			starter(dick)

	if dick['his']:
		url = u'/projects/{project_id!s}/?&cmdlog={command_name!s}{log_ids!s}{parameters!s}'.format(
			parameters=info(data, tab),
			project_id=project.id,
			log_ids=dick['logi'],
			command_name=name,
		)
	else:
		tab = data.get('tab')
		if tab == 'logs':
			tab = 'scripts'

		url = u'/command_log/?cmd={command_name!s}&tab={tab!s}&prid={project_id!s}{log_ids!s}{parameters!s}'.format(
			parameters=info(data, tab),
			project_id=project.id,
			log_ids=dick['logi'],
			command_name=name,
			tab=tab,
		)

	return url
