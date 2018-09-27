# -*- encoding: utf-8 -*-

from subprocess import call, check_output
from conf import dbname, dbhost, dbpass, dbport, dbuser


def psql(query, select=False):
	psql_opt = ['psql', '-U', dbuser, '-h', dbhost, '-p', dbport, '-d', dbname, '-tAc', query]
	if select:
		data = check_output(psql_opt, env={"PGPASSWORD": dbpass})
		return data
	else:
		error = call(psql_opt, env={"PGPASSWORD": dbpass})
		return error
