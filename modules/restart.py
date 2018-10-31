# -*- encoding: utf-8 -*-

from time import sleep
from stop import run as stop
from start import run as start


def description(args, log):
	log.write('\nRestart jboss on server %s\n' % args.server)


def run(args, log):

	error = stop(args, log)
	sleep(3)
	error += start(args, log)
	return error
