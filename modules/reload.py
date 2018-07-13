# -*- encoding: utf-8 -*-


def description(args):
	return "\nReload jboss config on server {server}\n".format(server=args.server)


def run(args):

	message = {'top': '\n<b>Выполняю jboss.reload</b>\n'.format(wdir=args.wdir), 'bot': ''}
	command = ['ssh', args.server, '{wdir}/jboss-bas-*/bin/jboss-cli.sh -c command=":reload"'.format(wdir=args.wdir)]
	dick = {'command': command, 'message': message}

	return dick
