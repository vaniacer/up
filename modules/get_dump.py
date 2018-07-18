# -*- encoding: utf-8 -*-

from datetime import datetime
from popen_call import my_call, message
from xml_parser import get_db_parameters
from download_upload import download_file


def description(args, log):
	log.write('\nGet database dump from server:\n%s' % args.server)


def run(args, log):

	filename = '{server}_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message('\n<b>Копирую дамп: {file}</b>\n'.format(file=filename), log)

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'dest': args.proname,
		'kill': True,
	}

	dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
		args.server, '{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir)
	)

	command = [
		'ssh', args.server,
		''' dbopts="-h {dbhost} -p {dbport} -U {dbuser}"
			PGPASSWORD="{dbpass}" pg_dump -Ox $dbopts -d {dbname} | gzip > "{file}" || {{
				error=$?
				printf "<b>Ошибка резервного копирования</b>"
				exit $error
			}}
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
	download_error = download_file(download, args.server, log)
	if download_error > 0:
		error = download_error

	message(
		""" \n<b>Files will be stored until tomorrow, please download them if you needed!</b>
			\n<a class='btn btn-primary' href='/download_dump/{pro}/{file}'>Download</a>
		""".format(file=filename, pro=args.proid), log
	)

	return error
