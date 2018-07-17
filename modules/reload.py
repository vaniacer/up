# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write('\nReload jboss config on server %s\n' % args.server)


def run(args, log, pid):

	message_top = ['printf', '\n<b>Выполняю jboss.reload</b>\n'.format(wdir=args.wdir)]
	my_popen(message_top, log, pid)

	command = ['ssh', args.server, '{wdir}/jboss-bas-*/bin/jboss-cli.sh -c command=":reload"'.format(wdir=args.wdir)]
	error = my_popen(command, log, pid)
	return error
