# -*- encoding: utf-8 -*-

from .models import Server, History, Job, Update, Script
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .permissions import check_perm_or404
from django.conf import settings as conf
from datetime import datetime, timedelta
from modules.uniq import uniq as uniqkey
from django.http import Http404
from os.path import join as opj
from subprocess import Popen
from re import escape


class CommandClass:
	"""Класс команды"""
	def __init__(
		self,
		permission='run_command',  # Permission needed to run this command.
		position=1,                # Position in commands list
		section='',                # Section command will be placed to(scripts, updates, dumps, cron, servers)
		style='',                  # Class assigned to a command button(for example 'danger')
		title='',                  # Pop up help message(via title)
		short='',                  # Short name for commands in quick section
		menu='',                   # Command name in UI
		name='',                   # Command name(an internal command name)
		run='',                    # Pre validation command, add "run_or_cron('RUN');" to prevent CRONing
		his=True,                  # If True, command log will be saved to history
		fst=False,                 # Add command to quick section
		dgr='false',               # If true will show confirmation window
		job='false',               # Check if some cron jobs selected
		srv='false',               # Check if some servers selected
		upd='false',               # Check if some updates selected
		scr='false',               # Check if some scripts selected
		dmp='false',               # Check if some dumps selected
	):
		self.permission = permission
		self.position = position
		self.section = section
		self.style = style
		self.title = title
		self.short = short
		self.name = name
		self.menu = menu
		self.run = run
		self.his = his
		self.fst = fst
		self.srv = srv
		self.upd = upd
		self.job = job
		self.scr = scr
		self.dmp = dmp
		self.dgr = dgr


commandick = {

	# Cron submenu }----------------------------------------------------------------------------------------------------
	'cancel_job': CommandClass(
		permission='run_cron',
		position=4,
		section='cron',
		title='Cancel selected cron job.',
		name='cancel_job',
		menu='Remove job',
		job='true',
		run="run_or_cron('RUN');",
	),

	'permanent_job': CommandClass(
		permission='run_cron',
		position=3,
		section='cron',
		title='Make selected cron job permanent.',
		name='permanent_job',
		menu='Run everyday',
		job='true',
		run="run_or_cron('RUN');",
	),

	'once_job': CommandClass(
		permission='run_cron',
		position=2,
		section='cron',
		title='Make selected cron job run once (default).',
		name='once_job',
		menu='Run one time',
		job='true',
		run="run_or_cron('RUN');",
	),

	'change_date': CommandClass(
		permission='run_cron',
		position=1,
		section='cron',
		title='Change selected cron job run date and time. If date\\time not set, it will set current date\\time.',
		name='change_date',
		menu='Change date',
		job='true',
		run="run_or_cron('RUN');",
	),

	# Dumps section }---------------------------------------------------------------------------------------------------
	'get_dump': CommandClass(
		permission='run_dump',
		section='dump',
		title='Get DB dump from selected server.',
		name='get_dump',
		menu='Get dump',
		srv='true',
	),

	'del_dump': CommandClass(
		permission='del_dump',
		position=20,
		section='dump',
		title='Delete selected dump from UpS.',
		name='del_dump',
		menu='Del dump',
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
	'update': CommandClass(
		permission='run_update',
		position=10,
		section='update',
		style='danger',
		title='Update selected server with selected update file.',
		name='update',
		menu='Start Update',
		srv='true',
		upd='true',
		dgr='true',
	),

	'copy': CommandClass(
		permission='run_update',
		position=20,
		section='update',
		title='Copy selected update to selected server.',
		name='copy',
		menu='Copy to server',
		srv='true',
	),

	'del_update': CommandClass(
		permission='del_update',
		position=30,
		section='update',
		title='Delete selected update from UpS.',
		name='del_update',
		menu='Delete from UpS',
		upd='true',
	),

	'del_sel_updates': CommandClass(
		permission='run_update',
		position=40,
		section='update',
		title='Delete selected update from selected server.',
		name='del_sel_updates',
		menu='Delete from server',
		srv='true',
		upd='true',
	),

	'del_all_updates': CommandClass(
		permission='run_update',
		position=50,
		section='update',
		title='Delete all updates from selected server.',
		name='del_all_updates',
		menu='Delete all from server',
		srv='true',
	),

	# Script section }--------------------------------------------------------------------------------------------------
	'run_script': CommandClass(
		permission='run_script',
		position=10,
		section='script',
		title='Run selected SH, PY or YML script on selected server.',
		name='run_script',
		menu='Run script',
		srv='true',
		scr='true',
	),

	'run_sql_script': CommandClass(
		permission='run_sql_script',
		position=20,
		section='script',
		title='Run selected SQL script on selected server.',
		name='run_sql_script',
		menu='Run sql script',
		srv='true',
		scr='true',
	),

	'del_script': CommandClass(
		permission='del_script',
		position=30,
		section='script',
		title='Delete selected script.',
		name='del_script',
		menu='Delete script',
		scr='true',
	),

	# Server section }--------------------------------------------------------------------------------------------------

	# Maintenance
	'maintenance_on': CommandClass(
		permission='maintenance',
		section='server',
		style='danger',
		title='Show "Maintenance" page on selected server.',
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
		title='Hide "Maintenance" page on selected server.',
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
		title='Reload jboss config on selected server.',
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
		title='Restart jboss on selected server.',
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
		title='Start jboss(krupd jboss.start) on selected server.',
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
		title='Stop jboss(krupd jboss.stop) on selected server.',
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
		title='Kill jboss(krupd jboss.kill) on selected server.',
		name='kill',
		menu='Kill jboss',
		srv='true',
		dgr='true',
	),

	# Info
	'server_info': CommandClass(
		permission='view_project',
		position=30,
		section='server',
		title='Show system info: CPU, mem, disk, port usage, users etc.',
		short='Info',
		name='server_info',
		menu='System Info',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
		fst=True,
	),

	'health_check': CommandClass(
		permission='view_project',
		position=35,
		section='server',
		title='Check if jboss process is running, bind port is active and accepts http connections.',
		short='Health',
		name='health_check',
		menu='Check health',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
		fst=True,
	),

	'check_conf': CommandClass(
		permission='check_conf',
		position=40,
		section='server',
		title='Show jboss.properties, standalone-full.xml and current java options.',
		short='Conf',
		name='check_conf',
		menu='Check conf',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
		fst=True,
	),

	# Logs
	'check_logs': CommandClass(
		permission='check_logs',
		position=50,
		section='server',
		title='Check logs.',
		short='Log',
		name='check_logs',
		menu='Check logs',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
		fst=True,
	),

	'check_GClog': CommandClass(
		permission='check_logs',
		position=51,
		section='server',
		title='Check GC log.',
		name='check_GClog',
		menu='Check GC log',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
	),

	'get_logs_day': CommandClass(
		permission='check_logs',
		position=52,
		section='server',
		title='Get day logs.',
		name='get_logs_day',
		menu='Get day logs',
		srv='true',
	),

	'get_logs_week': CommandClass(
		permission='check_logs',
		position=53,
		section='server',
		title='Get week logs.',
		name='get_logs_week',
		menu='Get week logs',
		srv='true',
	),

	'get_logs_month': CommandClass(
		permission='check_logs',
		position=54,
		section='server',
		title='Get month logs.',
		name='get_logs_month',
		menu='Get month logs',
		srv='true',
	),

	'get_logs_all': CommandClass(
		permission='check_logs',
		position=55,
		section='server',
		title='Get all logs. Careful there can be a LOT of logs!)',
		name='get_logs_all',
		menu='Get all logs',
		srv='true',
	),

	# Backup
	'backup_db': CommandClass(
		permission='make_backup',
		position=60,
		section='server',
		title='Database backup, files will be stored on the server and downloaded to UpS.',
		name='backup_db',
		menu='Backup base',
		srv='true',
	),

	'backup_sys': CommandClass(
		permission='make_backup',
		position=61,
		section='server',
		title='System backup files will be stored on the server and downloaded to UpS.',
		name='backup_sys',
		menu='Backup system',
		srv='true',
	),

	'backup_full': CommandClass(
		permission='make_backup',
		position=62,
		section='server',
		title='System and DB backup files will be stored on the server and downloaded to UpS.',
		name='backup_full',
		menu='Backup full',
		srv='true',
	),

	'copy_utils': CommandClass(
		permission='maintenance',
		position=70,
		section='server',
		title='Copy utils folder to selected server.',
		name='copy_utils',
		menu='Copy utils',
		srv='true',
	),

	'peep_pass': CommandClass(
		permission='peep_pass',
		position=75,
		section='server',
		title='Peep passwords from file krista-users.properties.',
		short='Pass',
		name='peep_pass',
		menu='Peep passwords',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
		fst=True,
	),

	'check_updates': CommandClass(
		permission='run_update',
		position=77,
		section='server',
		title='Check updates on selected server.',
		short='Updates',
		name='check_updates',
		menu='Check updates',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
		fst=True,
	),

	'tunnel': CommandClass(
		permission='tunnel',
		position=80,
		section='server',
		title='Make ssh tunnel to the bind port of selected server.',
		short='Tunnel',
		name='tunnel',
		menu='Create tunnel',
		run="run_or_cron('RUN');",
		srv='true',
		his=False,
	),

	'test_ssh': CommandClass(
		permission='tunnel',
		position=90,
		section='server',
		title='Test ssh connection.',
		short='Tunnel',
		name='test_ssh',
		menu='Test ssh',
		run="run_or_cron('RUN');",
		srv='true',
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


def date_validate(date, date_format):
	try:
		datetime.strptime(escape(date), date_format)
	except ValueError:
		raise Http404


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
		http=dick['http'],
	)


def starter(dick):
	"""Запускает выполнение комманды в фоновом процессе."""
	python = opj(conf.BASE_DIR, '../env/bin/python')
	opt = [
		python, 'starter.py', dick['cmnd'],
		'--name', str(dick['proj'].name),
		'--pid',  str(dick['proj'].id),
		'--key',  dick['uniq'],
		'--date', dick['cdat'],
	]

	opt.extend(dick['opt'])

	for ID in dick['data'].getlist('selected_updates'):
		dick['http'] += '&selected_updates={}'.format(ID)
		update = get_object_or_404(Update, id=ID)
		opt.extend(['-u', str(update.file)])

	for ID in dick['data'].getlist('selected_scripts'):
		dick['http'] += '&selected_scripts={}'.format(ID)
		script = get_object_or_404(Script, id=ID)
		opt.extend(['-x', str(script.file)])
		# split options string coz re.escape escapes spaces as well
		oplist = str(dick['data'].get('script_opt' + ID))
		dick['http'] += '&script_opt{id}={val}'.format(id=ID, val=oplist)
		oplist = oplist.split()
		# join it back and escape special symbols
		opdone = ' '.join(escape(opt) for opt in oplist)
		# add result as script arg -o 'test 123'
		opt.extend(['-o', opdone])

	for dump in dick['data'].getlist('selected_dbdumps'):
		dick['http'] += '&selected_dbdumps={}'.format(dump)
		opt.extend(['-d', str(dump)])

	if dick['his']:
		opt.extend(['--history'])
		add_event(dick)

	if conf.DEBUG:  # Print debug information in console if DEBUG = True
		print u'\n{l2}{{ Starter options }}{l2}\n{opt}\n{l2}{{ Full commandick }}{l2}\n{dick}\n{l1}\n'.format(
			dick=u'\n'.join(u'{K}:{V}'.format(K=key, V=val) for key, val in dick.iteritems()),
			l1='-' * 100,
			l2='-' * 40,
			opt=opt,
		)

	Popen(opt)


def run_cmd(data, project, user):
	"""Запускает выбранную команду."""
	tab = ''
	date = run_date()
	runt = data['run_type']
	name = data['run_cmnd']
	check_perm_or404('run_command', project, user)
	check_perm_or404(commandick[name].permission, project, user)
	http = u'/projects/{P}/?repeat=1&run_cmnd={C}&run_type=RUN'.format(C=name, P=project.id)

	if data.get('selected_date', default=None) and data.get('selected_time', default=None):
		date = '%s %s' % (data['selected_date'], data['selected_time'])
		date_validate(date, "%Y\\-%m\\-%d\\ %H\\:%M")

	dick = {
		'opt': [],
		'jobj': '',
		'cron': '',
		'uniq': '',
		'exit': '',
		'logi': '',
		'http': http,
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
			uniq = uniqkey()

			dick['opt'] = ['--job', jobi]
			dick['logi'] += '&logid=%s' % uniq
			dick.update({'cron': jobi, 'uniq': uniq, 'serv': serv, 'jobj': jobj})

			starter(dick)

	# Commands that can run without server
	elif dick['srv'] == 'false':

			uniq = uniqkey()

			dick.update({'uniq': uniq})
			dick['logi'] += '&logid=%s' % uniq

			starter(dick)

	# Server commands
	else:

		tab = 'logs'

		for server_id in data.getlist('selected_servers'):

			uniq = uniqkey()
			serv = get_object_or_404(Server, id=server_id)
			port = data.get('port') or serv.port

			dick['logi'] += '&logid=%s' % uniq
			dick.update({'uniq': uniq, 'serv': serv})
			dick['http'] = u'{http}&selected_servers={srv}'.format(http=http, srv=server_id)
			dick['opt'] = ['--server', serv.addr, '--wdir', serv.wdir, '--port', port]

			if runt == 'CRON':
				if not dick['his']:
					return back_url(data)

				dick.update({'cron': uniq, 'cdat': date})
				add_job(dick)

				dick['name'] = 'Set cron job - %s' % name.lower()
				dick['opt'].extend(['--cron'])

			starter(dick)

	if dick['his'] and not data.get('repeat'):
		url = u'/projects/{pid!s}/?&cmdlog={cmd!s}{log!s}{opt!s}'.format(
			opt=info(data, tab),
			log=dick['logi'],
			pid=project.id,
			cmd=name,
		)
	else:
		tab = data.get('tab', default='')
		if tab == 'logs':
			tab = 'scripts'

		url = u'/command_log/?cmd={cmd!s}&tab={tab!s}&prid={pid!s}{log!s}{opt!s}'.format(
			opt=info(data, tab),
			log=dick['logi'],
			pid=project.id,
			cmd=name,
			tab=tab,
		)

	return url
