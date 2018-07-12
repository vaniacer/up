# -*- encoding: utf-8 -*-

from datetime import datetime


def description(args):
	return "\nBackup database on server:\n%s" % args.server


def run(args):

	filename = '{server}_dbdump_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message = {
		'top': '\n<b>Копирую файл - {file}</b>\n'.format(file=filename),
		'bot':
			"""
			\n<b>File will be stored until tomorrow, please download it if you need this file!</b>
			\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>\n
			""".format(file=filename),
	}

	download = {
		'path': '{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename),
		'file': filename,
		'dest': '',
	}

	command = [
		'ssh', args.server,
		'''
		rawdta=$(grep '"DataaccessDS"' -A15  "{wdir}"/jboss-bas-*/standalone/configuration/standalone-full.xml)
		dbuser=${{rawdta//*<user-name>/}};   dbuser=${{dbuser//<\/user-name>*/}}
		dbpass=${{rawdta//*<password>/}};    dbpass=${{dbpass//<\/password>*/}}
		dbhost=${{rawdta//*:\/\//}};         dbhost=${{dbhost//:[0-9]*/}}
		dbport=${{rawdta//*${{dbhost}}:/}};  dbport=${{dbport//\/*/}}
		dbname=${{rawdta//*${{dbport}}\//}}; dbname=${{dbname//<*/}}
		dbopts="-h $dbhost -p $dbport -U $dbuser"
		
		PGPASSWORD="$dbpass" pg_dump -Ox $dbopts -d $dbname | gzip > "{file}" && printf "$file" || {{
			error=$?
			printf "<b>Ошибка резервного копирования</b>"
			exit $error
		}}
		'''.format(wdir=args.wdir, file=download['path']),
	]

	dick = {'command': command, 'message': message, 'download': download}

	return dick

