# -*- encoding: utf-8 -*-

from .backup_sys import run as sys_bkp
from .backup_db import run as db_bkp


def description(args, log):
	log.write("\nBackup database and system on server %s" % args.server)


def run(args, log):

	error = 0
	error += db_bkp(args,  log)
	error += sys_bkp(args, log)

	return error
