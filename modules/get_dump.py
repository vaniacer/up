# -*- encoding: utf-8 -*-

from datetime import datetime
from my_popen import my_popen
from xml_parser import parser
from download_upload import download_file
from subprocess import check_output


def description(args, log):
	log.write('\nGet database dump from server:\n%s' % args.server)


def run(args, log, pid):

	filename = '{server}_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message_top = ['printf', '\n<b>Копирую дамп: {file}</b>\n'.format(file=filename)]
	message_bot = [
		'printf',
		""" \n<b>Files will be stored until tomorrow, please download them if you needed!</b>
			\n<a class='btn btn-primary' href='/download_dump/{pro}/{file}'>Download</a>
		""".format(file=filename, pro=args.proid),
	]

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'dest': args.proname,
		'kill': True,
	}

	get_xml = [
		'ssh', args.server,
		'''cat {wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml
		'''.format(wdir=args.wdir)
	]
	xml = check_output(get_xml)
	dbhost, dbport, dbname, dbuser, dbpass = parser(xml)

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

	my_popen(message_top, log, pid)

	error = my_popen(command, log, pid)
	download_error = download_file(download, args.server, log)
	if download_error > 0:
		error = download_error

	my_popen(message_bot, log, pid)
	return error
