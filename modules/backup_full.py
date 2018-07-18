# -*- encoding: utf-8 -*-

from .backup_db import run as db_bkp
from .backup_sys import run as sys_bkp


def description(args, log):
	log.write("\nBackup database and system on server %s" % args.server)


def run(args, log):

	error = db_bkp(args, log)
	sys_error = sys_bkp(args, log)
	if sys_error > 0:
		error = sys_error

	return error
