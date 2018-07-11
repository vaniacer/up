# -*- encoding: utf-8 -*-


def description(args):
	return "\nBackup database on server:\n%s" % args.server


def run(args):

	command = [
		'''
		wdir="{wdir}"
		file="{server}_dbdump_`printf "%(%d-%m-%Y)T"`.gz"
		
		rawdta=$(grep '"DataaccessDS"' -A15 "$wdir"/jboss-bas-*/standalone/configuration/standalone-full.xml)
		dbuser=${{rawdta//*<user-name>/}};   dbuser=${{dbuser//<\/user-name>*/}}
		dbpass=${{rawdta//*<password>/}};    dbpass=${{dbpass//<\/password>*/}}
		dbhost=${{rawdta//*:\/\//}};         dbhost=${{dbhost//:[0-9]*/}}
		dbport=${{rawdta//*${{dbhost}}:/}};  dbport=${{dbport//\/*/}}
		dbname=${{rawdta//*${{dbport}}\//}}; dbname=${{dbname//<*/}}
		dbopts="-h $dbhost -p $dbport -U $dbuser"
		
		cd $wdir/backup
		
		PGPASSWORD="$dbpass" pg_dump -Ox $dbopts -d $dbname | gzip > "$file" && printf "$file" || {{
			error=$?
			printf "<b>Ошибка резервного копирования</b>"
			exit $error
		}}
		'''.format(wdir=args.wdir, server=args.server, key=args.key)
	]

	message = '\n-----{ <b>Server %s</b> }-----\n' % args.server

	return command, message

