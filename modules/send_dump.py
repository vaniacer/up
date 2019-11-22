# -*- encoding: utf-8 -*-

from download_upload import upload_file
from popen_call import my_call, message
from xml_parser import xml_parser
from up.settings import DUMP_DIR
from os.path import join as opj
from warning import warning


def description(args, log):
	log.write('\nCopy DB dump {dump} to server {server}\n'.format(dump=args.dump[0], server=args.server))


def run(args, log):

	error = 0
	filename = args.dump[0]
	dump = opj(DUMP_DIR, args.name, args.dump[0])
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	cnf_dir = '{wdir}/jboss-bas-*/standalone/configuration'.format(wdir=args.wdir)

	# --------------------------{ Add warning message with pause }---------------------------------------
	warning('You are sending dump - <b>{D}</b>\nto server - <b>{S}</b>'.format(S=args.server, D=filename), 30, log)

	message('\n<b>Копирую файл {}</b>\n'.format(filename), log)
	upload = {'file': [dump], 'dest': tmp_dir}
	error += upload_file(upload, args.server, log)

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
			dbopts="-h $dbhost -p $dbport -U $dbuser "
			dbconn="ALTER DATABASE $dbname ALLOW_CONNECTIONS false;"
			dbterm="SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$dbname';"

			psql     $dbopts -c "$dbconn" template1 || ((error+=$?))
			psql     $dbopts -c "$dbterm" template1 || ((error+=$?))
			dropdb   $dbopts     $dbname            || ((error+=$?))
			createdb $dbopts -O  $dbuser  $dbname   || ((error+=$?))

			gunzip -c {tmp}/{file} | psql -v ON_ERROR_STOP=1 $dbopts -d $dbname
			for i in ${{PIPESTATUS[@]}}; {{ ((error+=$i)); }}
			exit $error
		'''.format(
			parser=xml_parser,
			wdir=args.wdir,
			file=filename,
			conf=cnf_dir,
			tmp=tmp_dir,
		)
	]

	error += my_call(command, log)

	# ------------------{ Delete tmp folder }-----------------------------
	remove_tmp = ['ssh', args.server, 'rm -rf {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error
