# -*- encoding: utf-8 -*-

from datetime import datetime
from my_popen import my_popen
from xml_parser import parser
from download_upload import download_file
from subprocess import check_output


def description(args, log):
	log.write("\nBackup database on server %s" % args.server)


def run(args, log, pid):

	filename = '{server}_dbdump_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message_top = ['printf', '\n<b>Копирую файл - {file}</b>\n'.format(file=filename)]
	message_bot = [
		'printf',
		''' \n<b>File will be stored until tomorrow, please download it if you need this file!</b>
			\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>
		'''.format(file=filename)
	]

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'kill': False,
		'dest': '',
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
