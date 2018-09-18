# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nKill jboss on server {server}\n'.format(server=args.server))


def run(args, log):

	message('\n<b>Убиваю jboss</b>\n'.format(wdir=args.wdir), log)
	command = [
		'ssh', args.server,
		""" pid=($(ps axo pid,cmd | grep {wdir} | grep [j]ava)) \
			[[ -e /proc/$pid ]] && kill -9 $pid
		""".format(wdir=args.wdir)
	]

	error = my_call(command, log)
	return error
