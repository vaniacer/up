# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nReload jboss config on server %s\n' % args.server)


def run(args, log):

	message('\n<b>Выполняю jboss.reload</b>\n'.format(wdir=args.wdir), log)
	command = ['ssh', args.server, '{wdir}/jboss-bas-*/bin/jboss-cli.sh -c command=":reload"'.format(wdir=args.wdir)]
	error = my_call(command, log)
	return error
