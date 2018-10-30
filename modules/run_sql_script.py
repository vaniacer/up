# -*- encoding: utf-8 -*-

from subprocess import check_output, STDOUT, CalledProcessError
from xml_parser import get_db_parameters
from download_upload import upload_file
from popen_call import my_call, message
from up.settings import DUMP_DIR
from os.path import join as opj


def description(args, log):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	log.write('\nRun SQL script(s):\n{scripts}\non server {server}\n'.format(scripts=scripts, server=args.server))


def run(args, log):

	error = 0
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
		args.server,
		'{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir),
	)

	scripts = [script for script in args.script if '.sql' in script]  # create .sql list
	if not scripts:
		message('\n<b>В списке нет SQL скриптов.</b>\n', log)
		return 1

	message('\n<b>Копирую файл(ы):</b>\n', log)
	upload = {'file': scripts, 'dest': tmp_dir}
	error += upload_file(upload, args.server, log)

	for script in scripts:

		with open(script) as f:
			body = f.read()

		filename = script.split('/')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		message('\n<b>Выполняю скрипт {file}, тело скрипта:</b>\n<i>{body}</i>\n\n<b>Результат:</b>\n'.format(
			file=filename,
			body=body,
		), log)

		# ------------------{ Run SQL script }---------------------------------
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

	remove_tmp = ['ssh', args.server, 'rm -rf {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error
