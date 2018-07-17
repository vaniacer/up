# -*- encoding: utf-8 -*-

from start import run as start
from stop import run as stop


def description(args, log):
	log.write('\nRestart jboss on server %s\n' % args.server)


def run(args, log, pid):

	error = stop(args, log, pid)
	start_error = start(args, log, pid)
	if start_error > 0:
		error = start_error
	return error
