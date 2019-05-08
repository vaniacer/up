# -*- encoding: utf-8 -*-

from xml_parser import get_db_parameters
from popen_call import my_call


def description(args, log):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	log.write('\nRun SQL script(s):\n{scripts}\non server {server}\n'.format(scripts=scripts, server=args.server))


def run(args, log):

	error = 0
	dbhost, dbport, dbname, dbuser, dbpass = get_db_parameters(
		args.server,
		'{wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml'.format(wdir=args.wdir),
	)
	# ------------------{ Run SQL query }---------------------------------
	command = [
		'ssh', args.server,
		''' export PGPASSWORD="{dbpass}"
			printf -- '-----{{ <b>Server {server}</b> }}-----\n\n'
			psql -h {dbhost} -p {dbport} -U {dbuser} -d {dbname} -tc "{query}"
		'''.format(
			query="select value from b_settings_param where name='Версия';",
			server=args.server,
			dbhost=dbhost,
			dbport=dbport,
			dbuser=dbuser,
			dbpass=dbpass,
			dbname=dbname,
		)
	]

	error += my_call(command, log)

	return error
