# -*- encoding: utf-8 -*-


def description(args):
	return "\nRestart jboss on server {server}\n".format(server=args.server)


def run(args):

	message = {'top': '\n<b>Выполняю jboss.stop & jboss.start</b>\n'.format(wdir=args.wdir), 'bot': ''}
	command = ['ssh', args.server, '{wdir}/krupd jboss.stop; {wdir}/krupd jboss.start'.format(wdir=args.wdir)]
	dick = {'command': command, 'message': message}

	return dick
