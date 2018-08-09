# -*- encoding: utf-8 -*-

from datetime import datetime
from popen_call import my_call, message
from xml_parser import get_db_parameters
from download_upload import download_file


def description(args, log):
	log.write("\nBackup database on server %s" % args.server)


def run(args, log):

	filename = '{server}_dbdump_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message('\n<b>Копирую файл {file}</b>\n'.format(file=filename), log)

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'kill': False,
		'dest': '',
	}

	dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
		args.server, '{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir)
	)

	command = [
		'ssh', args.server,
		''' dbopts="-h {dbhost} -p {dbport} -U {dbuser}"
			PGPASSWORD="{dbpass}" pg_dump -Ox $dbopts -d {dbname} | gzip > "{file}"
			for i in ${{PIPESTATUS[@]}}; {{ ((error+=$i)); }}; exit $error
		'''.format(
			file=download['file'][0],
			wdir=args.wdir,
			dbhost=dbhost,
			dbport=dbport,
			dbuser=dbuser,
			dbpass=dbpass,
			dbname=dbname,
		)
	]

	error = my_call(command, log)
	if error == 0:
		download_error = download_file(download, args.server, log)
		if download_error > 0:
			error = download_error

		message(
			''' \n<b>File will be stored until tomorrow, please download it if you need this file!</b>
				\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>
			'''.format(file=filename), log
		)

	return error
