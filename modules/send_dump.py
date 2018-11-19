# -*- encoding: utf-8 -*-

from warning import warning
from os.path import join as opj
from up.settings import DUMP_DIR
from download_upload import upload_file
from popen_call import my_call, message
from xml_parser import get_db_parameters


def description(args, log):
	log.write('\nCopy DB dump {dump} to server {server}\n'.format(dump=args.dump[0], server=args.server))


def run(args, log):

	filename = args.dump[0]
	dump = opj(DUMP_DIR, args.proname, args.dump[0])
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)

	warning('You are sending dump - <b>{dump}</b>\nto server - <b>{server}</b>'.format(
		server=args.server,
		dump=filename,
	), 30, log)

	message('\n<b>Копирую файл {}</b>\n'.format(filename), log)
	upload = {'file': [dump], 'dest': tmp_dir}
	error = upload_file(upload, args.server, log)

	dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
		args.server, '{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir)
	)

	command = [
		'ssh', args.server,
		''' dbopts="-h {dbhost} -p {dbport} -U {dbuser}"

			dbconn="ALTER DATABASE {dbname} ALLOW_CONNECTIONS false;"
			dbterm="SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{dbname}';"

			PGPASSWORD="{dbpass}" psql     $dbopts -c "$dbconn"          &> /dev/null
			PGPASSWORD="{dbpass}" psql     $dbopts -c "$dbterm"          || error=$?
			PGPASSWORD="{dbpass}" dropdb   $dbopts     {dbname}          || error=$?
			PGPASSWORD="{dbpass}" createdb $dbopts -O  {dbuser} {dbname} || error=$?

			gunzip -c {tmp}/{file} | PGPASSWORD="{dbpass}" psql -v ON_ERROR_STOP=1 $dbopts -d {dbname}
			for i in ${{PIPESTATUS[@]}}; {{ ((error+=$i)); }}; exit $error
		'''.format(
			wdir=args.wdir,
			file=filename,
			dbhost=dbhost,
			dbport=dbport,
			dbuser=dbuser,
			dbpass=dbpass,
			dbname=dbname,
			tmp=tmp_dir,
		)
	]

	cmd_error = my_call(command, log)
	if cmd_error > 0:
		error = cmd_error
	return error
