# -*- encoding: utf-8 -*-

from popen_call import my_call


def description(args, log):
	log.write("\nShow logs of server %s" % args.server)


def run(args, log):

	command = [
		'ssh', args.server,
		''' printf '\n-----{{ <b>Server {server}</b> }}-----\n'
			cat {wdir}/jboss-bas-*/standalone/log/server.log | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'
		'''.format(wdir=args.wdir, server=args.server)
	]

	error = my_call(command, log)
	return error
