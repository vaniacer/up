# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write("\nShow updates on server %s" % args.server)


def run(args, log, pidfile):

	command = [
		'ssh', args.server,
		'''printf '\n-----{{ <b>Server {server}</b> }}-----\n'
		
		printf '\nПакеты обновлений:\n'
		ls {wdir}/updates/new
		'''.format(wdir=args.wdir, server=args.server)
	]

	error = my_popen(command, log, pidfile)
	return error
