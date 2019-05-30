# -*- encoding: utf-8 -*-

from datetime import datetime
from popen_call import my_call, message
from download_upload import download_file


def description(args, log):
	log.write('\nShow GC log from server:\n%s' % args.server)


def run(args, log):

	command = [
		'ssh', args.server,
		''' printf '\n-----{{ <b>Server {server}</b> }}-----\n'
			cat {wdir}/jboss-bas-*/standalone/log/gc.log*
		'''.format(wdir=args.wdir, server=args.server)
	]

	error = my_call(command, log)
	return error
