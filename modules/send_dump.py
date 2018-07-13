# -*- encoding: utf-8 -*-

import os
from up.settings import DUMP_DIR


def description(args):
	return "\nCopy DB dump {dump} to server {server}\n".format(dump=args.dump[0], server=args.server)


def run(args):

	filename = args.dump[0]
	dump = os.path.join(DUMP_DIR, args.proname, args.dump[0])
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)

	message = {'top': '\n<b>Копирую файл {}</b>\n'.format(filename), 'bot': ''}
	upload = {'file': [dump], 'dest': tmp_dir}
	command = [
		'ssh', args.server,
		'''
		rawdta=$(grep '"DataaccessDS"' -A15  {wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml)
		dbuser=${{rawdta//*<user-name>/}};   dbuser=${{dbuser//<\/user-name>*/}}
		dbpass=${{rawdta//*<password>/}};    dbpass=${{dbpass//<\/password>*/}}
		dbhost=${{rawdta//*:\/\//}};         dbhost=${{dbhost//:[0-9]*/}}
		dbport=${{rawdta//*${{dbhost}}:/}};  dbport=${{dbport//\/*/}}
		dbname=${{rawdta//*${{dbport}}\//}}; dbname=${{dbname//<*/}}
		dbopts="-h $dbhost -p $dbport -U $dbuser"

		dbterm="ALTER DATABASE $dbname ALLOW_CONNECTIONS false;
				SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$dbname';"

		PGPASSWORD="$dbpass" psql     $dbopts -c "$dbterm" || error=$?
		PGPASSWORD="$dbpass" dropdb   $dbopts     $dbname  || error=$?
		PGPASSWORD="$dbpass" createdb $dbopts -O  $dbuser $dbname || error=$?
		gunzip -c {tmp}/{file} | PGPASSWORD="$dbpass" psql -v ON_ERROR_STOP=1 $dbopts -d $dbname || error=$?
		rm -r {tmp}
		exit $error
		'''.format(file=filename, wdir=args.wdir, tmp=tmp_dir)
	]

	dick = {'command': command, 'message': message, 'upload': upload}

	return dick
