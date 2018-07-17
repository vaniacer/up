# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write('\nStart jboss on server %s\n' % args.server)


def run(args, log, pid):

	message_top = ['printf', '\n<b>Выполняю jboss.start</b>\n'.format(wdir=args.wdir)]
	my_popen(message_top, log, pid)

	command = ['ssh', args.server, '{wdir}/krupd jboss.start'.format(wdir=args.wdir)]
	error = my_popen(command, log, pid)
	return error
