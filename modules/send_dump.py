# -*- encoding: utf-8 -*-

import os
from up.settings import DUMP_DIR


def description(args):
	return "\nCopy DB dump {dump} to server {server}\n".format(dump=args.dump[0], server=args.server)


def run(args):

	dump = os.path.join(DUMP_DIR, args.proname, args.dump[0])
	message = {'top': '\n<b>Копирую файл {file}</b>\n'.format(file=dump), 'bot': ''}

	command = [
		'rsync', '-e', 'ssh', '--progress', '-lzuogthvr', dump,
		'{addr}:{wdir}/temp/{key}/'.format(key=args.key, addr=args.server, wdir=args.wdir),

		'ssh', args.server,
		'''
		rawdta=$(grep '"DataaccessDS"' -A15  "{wdir}"/jboss-bas-*/standalone/configuration/standalone-full.xml)
		dbuser=${{rawdta//*<user-name>/}};   dbuser=${{dbuser//<\/user-name>*/}}
		dbpass=${{rawdta//*<password>/}};    dbpass=${{dbpass//<\/password>*/}}
		dbhost=${{rawdta//*:\/\//}};         dbhost=${{dbhost//:[0-9]*/}}
		dbport=${{rawdta//*${{dbhost}}:/}};  dbport=${{dbport//\/*/}}
		dbname=${{rawdta//*${{dbport}}\//}}; dbname=${{dbname//<*/}}
		dbopts="-h $dbhost -p $dbport -U $dbuser"

		PGPASSWORD="$dbpass" gunzip -c {wdir}/temp/{file} | psql -h $dbopts -d $dbname || {{
			error=$?
			printf "<b>Ошибка восстановления базы</b>"
			rm - {wdir}/temp/{key}
			exit $error
		}}
		rm -r {wdir}/temp/{key}
		'''.format(file=dump, wdir=args.wdir, key=args.key)
	]

	dick = {'command': command, 'message': message, 'download': ''}

	return dick
