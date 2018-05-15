# -*- encoding: utf-8 -*-

from .commands_engine import get_key, starter, add_event, add_job
from .permissions import check_perm_or404
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
		'tag': False,                             # Show or not html tags in command log
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
		'tag': False,
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
		'tag': False,
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
		'tag': False,
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
		'dmp': 'true',
		'dgr': 'false',
		'run': '',
		'history': True,
		'tag':  True,
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
		'tag': False,
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
		'tag':  True,
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
		'tag': False,
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
		'tag': False,
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
		'tag': True,
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
		'tag': False,
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
		'tag': False,
	},

	# Script section }--------------------------------------------------------------------------------------------------
	'py_script': {
		'name': 'py_script',
		'position': 10,
		'section': 'script',
		'title': 'Run selected python script(s) on selected server(s).',
		'class': '',
		'menu': 'Run Python script',
		'bash': 'script_python.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'true',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'history': True,
		'tag':  True, },

	'bash_script': {
		'name': 'bash_script',
		'position': 20,
		'section': 'script',
		'title': 'Run selected bash script(s) on selected server(s).',
		'class': '',
		'menu': 'Run BASH script',
		'bash': 'script_bash.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'true',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'history': True,
		'tag': True,
	},

	'yml_script': {
		'name': 'yml_script',
		'position': 30,
		'section': 'script',
		'title': 'Run selected yml playbook(s) on selected server(s).',
		'class': '',
		'menu': 'Run YAML script',
		'bash': 'script_yml.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'true',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'history': True,
		'tag': False,
	},

	'sql_script': {
		'name': 'sql_script',
		'position': 40,
		'section': 'script',
		'title': 'Run selected sql script(s) on selected server(s).',
		'class': '',
		'menu': 'Run SQL script',
		'bash': 'script_sql.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'true',
		'dmp': 'false',
		'dgr': 'false',
		'run': '',
		'history': True,
		'tag': True,
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
		'tag': False,
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
		'tag': False,
	},

	# Jboss
	'reload': {
		'name': 'reload',
		'position': 20,
		'section': 'server',
		'title': 'Reload jboss config on selected server(s).',
		'class': 'danger',
		'menu': 'Reload config',
		'bash': 'reload.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'history': True,
		'tag': False,
	},

	'restart': {
		'name': 'restart',
		'position': 21,
		'section': 'server',
		'title': 'Restart jboss on selected server(s).',
		'class': 'danger',
		'menu': 'Restart jboss',
		'bash': 'restart.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'history': True,
		'tag': False,
	},

	'start': {
		'name': 'start',
		'position': 22,
		'section': 'server',
		'title': 'Start jboss(krupd jboss.start) on selected server(s).',
		'class': 'danger',
		'menu': 'Start jboss',
		'bash': 'start.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'history': True,
		'tag': False,
	},

	'stop': {
		'name': 'stop',
		'section': 'server',
		'position': 23,
		'title': 'Stop jboss(krupd jboss.stop) on selected server(s).',
		'class': 'danger',
		'menu': 'Stop jboss',
		'bash': 'stop.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'history': True,
		'tag': False,
	},

	'kill': {
		'name': 'kill',
		'position': 24,
		'section': 'server',
		'title': 'Kill jboss(krupd jboss.kill) on selected server(s).',
		'class': 'danger',
		'menu': 'Kill jboss',
		'bash': 'kill.sh',
		'srv': 'true',
		'upd': 'false',
		'job': 'false',
		'scr': 'false',
		'dmp': 'false',
		'dgr': 'true',
		'run': '',
		'history': True,
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
		'history': False,
		'tag':  True,
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
		'tag': False,
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
		'tag': False,
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
		'tag': True,
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
		'tag': True,
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
		'tag':  True,
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
		'tag':  True,
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
		'tag':  True,
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
		'tag': False,
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
		'tag': True,
	},
}


def command(selected):
	"""Определяет bash script по полученному command name."""
	cmd = ''.join(selected['command'])
	selected['cmdname'] = commandick[cmd]['bash']
	selected['history'] = commandick[cmd]['history']
	return commandick[cmd]['tag'], selected['history']


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
		url += '#%s' % data.get('tab')
	return url


def run_date():
	"""Если не указана дата, возвращает текущую дату + 1 минута."""
	date = datetime.datetime.now() + datetime.timedelta(minutes=1)
	return date.strftime("%Y-%m-%d %H:%M")


def cmd_run(data, project, user):
	"""Запускает выбранную команду."""
	check_perm_or404('run_command', project, user)

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
		if not his:
			return '/projects/%s/?%s' % (project.id, info(data))
		selected['cid'] = add_job(selected, 'Working...', key)
		selected['name'] = 'Set cron job - %s' % selected['command'].lower()
	if his:
		selected['hid'] = add_event(selected, 'Working...', '', crn, date)
	starter(selected)

	url = '/command_log/?cmd=%s&rtype=%s&hid=%s&cid=%s&tab=%s&prid=%s&timedate=%s&logid=%s%s' % (
		selected['command'],
		selected['rtype'],
		selected['hid'],
		selected['cid'],
		data.get('tab'),
		project.id,
		date,
		key,
		info(data),
	)

	return url
