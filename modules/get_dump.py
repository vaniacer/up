# -*- encoding: utf-8 -*-

from download_upload import download_file
from popen_call import my_call, message
from xml_parser import xml_parser
from modules.uniq import uniq
from datetime import datetime


def description(args, log):
	log.write('\nGet database dump from server:\n%s' % args.server)


def run(args, log):

	filename = '{server}_dbdump_{date:%d-%m-%Y_%H%M}.gz'.format(server=args.server, date=datetime.now())
	cnf_dir = '{wdir}/jboss-bas-*/standalone/configuration'.format(wdir=args.wdir)

	message('\n<b>Копирую файл {file}</b>\n'.format(file=filename), log)
	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'dest': args.name,
		'kill': True,
	}

	command = [
		'ssh', args.server,
		''' cd {conf}
			data=($(python -c "{parser}"))
			dbhost=${{data[0]}}
			dbport=${{data[1]}}
			dbname=${{data[2]}}
			dbuser=${{data[3]}}
			dbpass=${{data[4]}}
			cd - &> /dev/null

			export PGPASSWORD="$dbpass"
			dbopts="-h $dbhost -p $dbport -U $dbuser -d $dbname"
			
			pg_dump -Ox $dbopts | gzip > "{file}"
			for i in ${{PIPESTATUS[@]}}; {{ ((error+=$i)); }}
			exit $error
		'''.format(
			file=download['file'][0],
			parser=xml_parser,
			wdir=args.wdir,
			conf=cnf_dir,
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
						value="curl {OP} https://ups.krista.ru/dumps/{PN}/{FN} | zcat | psql testdb" id="{ID}">
						<input onclick="copy_to_clipboard('{ID}')" type="button" value="Copy" class="btn btn-primary"
						title="Copy to clipboard"/>
					</div>
				</div>
			""".format(
				OP='-o- --noproxy ups.krista.ru --netrc-file ~/.ups_download',
				PN=args.name,
				PI=args.pid,
				FN=filename,
				ID=uniq(),
			), log
		)
	return error
