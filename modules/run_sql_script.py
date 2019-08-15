# -*- encoding: utf-8 -*-

from download_upload import upload_file, download_file
from xml_parser import get_db_parameters
from popen_call import my_call, message
from up.settings import DUMP_DIR


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

		filename = script.split('/')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		log_path = '{tmp}/{file}_{srv}.log'.format(tmp=tmp_dir, file=filename, srv=args.server)

		# ------------------{ Run SQL script }---------------------------------
		command = [
			'ssh', args.server,
			''' export PGPASSWORD="{dbpass}"
				dbopts="-h {dbhost} -p {dbport} -U {dbuser}"
				
				printf "\n<b>Выполняю скрипт {name}, тело скрипта:</b>\n<i>"
				cat "{file}"

				psql -v ON_ERROR_STOP=1 $dbopts -d {dbname} < "{file}" &> {log}
				
				printf "</i>\n\n<b>Результат:</b>\n"
				cat {log}
			'''.format(
				wdir=args.wdir,
				name=filename,
				file=filepath,
				dbhost=dbhost,
				dbport=dbport,
				dbuser=dbuser,
				dbpass=dbpass,
				dbname=dbname,
				log=log_path,
			)
		]

		error += my_call(command, log)
		download = {'file': [log_path], 'dest': DUMP_DIR, 'kill': False}
		error += download_file(download, args.server, log, link=True, silent=True)

	remove_tmp = ['ssh', args.server, 'rm -rf {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error
