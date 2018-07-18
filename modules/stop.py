# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nStop jboss on server %s\n' % args.server)


def run(args, log):

	message('\n<b>Выполняю jboss.stop</b>\n'.format(wdir=args.wdir), log)
	command = ['ssh', args.server, '{wdir}/krupd jboss.stop'.format(wdir=args.wdir)]
	error = my_call(command, log)
	return error
