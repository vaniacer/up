# -*- encoding: utf-8 -*-

from datetime import datetime
from popen_call import my_call, message
from xml_parser import get_db_parameters
from download_upload import download_file


def description(args, log):
	log.write('\nGet database dump from server:\n%s' % args.server)


def run(args, log):

	filename = '{server}_dbdump_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message('\n<b>Копирую файл {file}</b>\n'.format(file=filename), log)

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'dest': args.name,
		'kill': True,
	}

	dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
		args.server, '{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir)
	)

	command = [
		'ssh', args.server,
		''' export PGPASSWORD="{dbpass}"
			dbopts="-h {dbhost} -p {dbport} -U {dbuser}"
			pg_dump -Ox $dbopts -d {dbname} | gzip > "{file}"
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
		error += download_file(download, args.server, log)

		message(
			""" \n<a class='btn btn-primary' href='/download_dump/{PI}/{FN}'>Download</a>
				\n<b>Команда для быстрого разворачивания дампа(Linux):</b>
				<div class="input-group col-md-10">
					<div class="input-group-btn">
						<input class="form-control" type="text"
						value="curl {OP} https://ups.krista.ru/dumps/{PN}/{FN} | zcat | psql testdb" id="DBC">
						<input onclick="copy_to_clipboard('DBC')" type="button" value="Copy" class="btn btn-primary"
						title="Copy to clipboard"/>
					</div>
				</div>
			""".format(
				OP='-o- --noproxy ups.krista.ru --netrc-file ~/.ups_download',
				PN=args.name,
				PI=args.pid,
				FN=filename,
			), log
		)

	return error
