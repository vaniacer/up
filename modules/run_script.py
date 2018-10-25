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
	updates = None
	home = expanduser('~')
	upd_dir = '{wdir}/updates/new'.format(wdir=args.wdir)
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	dbhost, dbport, dbname, dbuser, dbpass = '', '', '', '', ''

	if any(".sql" in s for s in args.script):
		dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
			args.server, '{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir)
		)

	files_to_upload = [script for script in args.script if '.yml' not in script]  # remove .yml from list
	if files_to_upload:
		message('\n<b>Копирую файл(ы):</b>\n', log)
		upload = {'file': files_to_upload, 'dest': tmp_dir}
		error += upload_file(upload, args.server, log)

	if args.update:
		upload = {'file': args.update, 'dest': upd_dir}
		updates = ['{dir}/{upd}'.format(dir=upd_dir, upd=update.split('/')[-1]) for update in args.update]
		error += upload_file(upload, args.server, log)

	for script, options in zip(args.script, args.options):

		with open(script) as f:
			body = f.read()

		filename = script.split('/')[-1]
		script_type = script.split('.')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		message('\n<b>Выполняю скрипт {file}, тело скрипта:</b>\n<i>{body}</i>\n\n<b>Результат:</b>\n'.format(
			file=filename,
			body=body,
		), log)

		if updates:
			options += ' '.join(updates)

		# ------------------{ Run bash script }--------------------------------
		if script_type == 'sh':
			command = [
				'ssh', args.server, 'cd {wdir}; bash {file} {options}'.format(
					options=options,
					wdir=args.wdir,
					file=filepath,
				)
			]
			error += my_call(command, log)

		# ------------------{ Run python script }------------------------------
		elif script_type == 'py':
			command = [
				'ssh', args.server, 'cd {wdir}; python {file} {options}'.format(
					options=options,
					wdir=args.wdir,
					file=filepath,
				)
			]
			error += my_call(command, log)

		# ------------------{ Run YML script }---------------------------------
		elif script_type == 'yml':
			command = [
				'ansible-playbook', script, '-i', '%s,' % args.server,
				'--vault-password-file', '%s/vault.txt' % home, '--syntax-check'
			]
			syntax_check = my_call(command, log)
			if syntax_check == 0:
				error += my_call(command[0:-1], log)  # run without '--syntax-check'

		# ------------------{ Run SQL script }---------------------------------
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
				error += e.returncode

		# ------------------{ Unknown script type }----------------------------
		else:
			message('\nUnknown script type.\n', log)
			error += 1

	remove_tmp = ['ssh', args.server, 'rm -rf {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error
