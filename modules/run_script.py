# -*- encoding: utf-8 -*-

from subprocess import check_output, STDOUT, CalledProcessError
from os.path import expanduser, join as opj
from xml_parser import get_db_parameters
from download_upload import upload_file
from popen_call import my_call, message
from up.settings import DUMP_DIR


def description(args, log):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	log.write('\nRun script(s):\n{scripts}\non server {server}\n'.format(scripts=scripts, server=args.server))


def run(args, log):

	error = 0
	home = expanduser('~')
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	dbhost, dbport, dbname, dbuser, dbpass = '', '', '', '', ''

	if any(".sql" in s for s in args.script):
		dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
			args.server, '{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir)
		)

	if any(".yml" in s for s in args.script):
		pass

	upload = {'file': args.script, 'dest': tmp_dir}
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	message('\n<b>Копирую файл(ы):\n{}</b>\n'.format(scripts), log)
	up_error = upload_file(upload, args.server, log)
	if up_error > 0:
		error = up_error

	for script in args.script:
		filename = script.split('/')[-1]
		script_type = script.split('.')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		message('\n<b>Выполняю скрипт {file}</b>\n'.format(file=filename), log)

		if script_type == 'sh':
			command = ['ssh', args.server, 'cd {wdir}; bash {file}'.format(file=filepath, wdir=args.wdir)]
			sh_error = my_call(command, log)
			if sh_error > 0:
				error = sh_error
		elif script_type == 'py':
			command = ['ssh', args.server, 'cd {wdir}; python {file}'.format(file=filepath, wdir=args.wdir)]
			py_error = my_call(command, log)
			if py_error > 0:
				error = py_error
		elif script_type == 'yml':
			command = [
				'ansible-playbook', script, '-i', '%s,' % args.server,
				'--vault-password-file', '%s/vault.txt' % home, '--syntax-check'
			]
			yml_error = my_call(command, log)
			if yml_error == 0:
				yml_error = my_call(command[0:-1], log)
			if yml_error > 0:
				error = yml_error
		elif script_type == 'sql':
			command = [
				'ssh', args.server,
				''' dbopts="-h {dbhost} -p {dbport} -U {dbuser}"
					PGPASSWORD="{dbpass}" psql -v ON_ERROR_STOP=1 $dbopts -d {dbname} < "{file}"
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

			try:
				sql_result = check_output(command, stderr=STDOUT)
				log_name = '{file}_{key}.log'.format(file=filename, key=args.key)
				with open(opj(DUMP_DIR, log_name), 'w') as f:
					f.write(sql_result)
				message(
					''' {sql}\n<b>Log will be stored until tomorrow, download it please if you need it!</b>
						\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>
					'''.format(file=log_name, sql=sql_result), log
				)
			except CalledProcessError as e:
				message(e.output, log)
				error = e.returncode

	remove_tmp = ['ssh', args.server, 'rm -r {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error
