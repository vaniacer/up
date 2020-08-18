# -*- encoding: utf-8 -*-

from download_upload import download_file
from popen_call import my_call, message
from xml_parser import xml_parser
from datetime import datetime


def description(args, log):
	log.write("\nBackup database on server %s" % args.server)


def run(args, log):

	error = 0
	filename = '{server}_dbdump_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	cnf_dir = '{wdir}/jboss-bas-*/standalone/configuration'.format(wdir=args.wdir)
	message('\n<b>Копирую файл {file}</b>\n'.format(file=filename), log)

	download = {'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)], 'dest': ''}
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

	error += my_call(command, log)
	if error == 0:
		error += download_file(download, args.server, log, link=True, limit=args.limit)

	return error
