# -*- encoding: utf-8 -*-

from time import sleep
from stop import run as stop
from kill import run as kill
from start import run as start


def description(args, log):
	log.write('\nRestart jboss on server %s\n' % args.server)


def run(args, log):

	error = stop(args, log)
	if error:
		error += kill(args, log)
	error += start(args, log)
	return error
