# -*- encoding: utf-8 -*-

from popen_call import my_call


def description(args, log):
	log.write("\nShow updates on server %s" % args.server)


def run(args, log):

	command = [
		'ssh', args.server,
		''' printf '\n-----{{ <b>Server {server}</b> }}-----\n'
			printf '\nПакеты обновлений:\n'
			ls {wdir}/updates/new
		'''.format(wdir=args.wdir, server=args.server)
	]

	error = my_call(command, log)
	return error
