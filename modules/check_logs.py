# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write("\nShow logs of server %s" % args.server)


def run(args, log, pidfile):

	command = [
		'ssh', args.server,
		''' printf '\n-----{{ <b>Server {server}</b> }}-----\n'
			cat {wdir}/jboss-bas-*/standalone/log/server.log
		'''.format(wdir=args.wdir, server=args.server)
	]

	error = my_popen(command, log, pidfile)
	return error
