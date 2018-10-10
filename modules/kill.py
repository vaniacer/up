# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nKill jboss on server {server}\n'.format(server=args.server))


def run(args, log):

	message('\n<b>Выполняю jboss.kill</b>\n'.format(wdir=args.wdir), log)
	command = ['ssh', args.server, '{wdir}/krupd jboss.kill'.format(wdir=args.wdir)]
	error = my_call(command, log)
	return error
