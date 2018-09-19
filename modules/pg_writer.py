# -*- encoding: utf-8 -*-

from subprocess import call
from conf import dbname, dbhost, dbpass, dbport, dbuser


def psql(query):
	psql_opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-c', query]
	error = call(psql_opt, env={"PGPASSWORD": dbpass})
	return error
