# -*- encoding: utf-8 -*-

from download_upload import upload_file
from subprocess import check_output
from os.path import expanduser
from my_popen import my_popen
from xml_parser import parser


def description(args, log):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	log.write('\nRun script(s):\n{scripts}\non server {server}\n'.format(scripts=scripts, server=args.server))


def run(args, log, pid):

	error = 0
	home = expanduser('~')
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	dbhost, dbport, dbname, dbuser, dbpass = '', '', '', '', ''

	if any(".sql" in s for s in args.script):
		get_xml = [
			'ssh', args.server,
			'''cat {wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml
			'''.format(wdir=args.wdir)
		]

		xml = check_output(get_xml)
		dbhost, dbport, dbname, dbuser, dbpass = parser(xml)

	if any(".yml" in s for s in args.script):
		pass

	upload = {'file': args.script, 'dest': tmp_dir}
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	message_top = ['printf', '\n<b>Копирую файл(ы):\n{}</b>\n'.format(scripts)]
	my_popen(message_top, log, pid)

	up_error = upload_file(upload, args.server, log)
	if up_error > 0:
		error = up_error

	for script in args.script:
		filename = script.split('/')[-1]
		script_type = script.split('.')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		message = ['printf', '\n<b>Выполняю скрипт {file}</b>\n'.format(file=filename)]
		my_popen(message, log, pid)

		if script_type == 'sh':
			command = ['ssh', args.server, 'cd {wdir}; bash {file}'.format(file=filepath, wdir=args.wdir)]
			sh_error = my_popen(command, log, pid)
			if sh_error > 0:
				error = sh_error
		elif script_type == 'py':
			command = ['ssh', args.server, 'cd {wdir}; python {file}'.format(file=filepath, wdir=args.wdir)]
			py_error = my_popen(command, log, pid)
			if py_error > 0:
				error = py_error
		elif script_type == 'yml':
			command = ['ansible-playbook', '--vault-password-file', '%s/vault.txt' % home, '-i', args.server, script]
			yml_error = my_popen(command, log, pid)
			if yml_error > 0:
				error = yml_error
		elif script_type == 'sql':
			command = [
				'ssh', args.server,
				''' dbopts="-h {dbhost} -p {dbport} -U {dbuser}"
					PGPASSWORD="{dbpass}" pg_dump -v ON_ERROR_STOP=1 -Ox $dbopts -d {dbname} < "{file}" || {{
						error=$?
						printf "<b>Ошибка в скрипте</b>"
						exit $error
					}}
				'''.format(
					wdir=args.wdir,
					file=filepath,
					dbhost=dbhost,
					dbport=dbport,
					dbuser=dbuser,
					dbpass=dbpass,
					dbname=dbname,
				)
			]
			sql_error = my_popen(command, log, pid)
			if sql_error > 0:
				error = sql_error

	remove_tmp = ['ssh', args.server, 'rm -r {tmp}'.format(tmp=tmp_dir)]
	my_popen(remove_tmp, log, pid)
	return error
