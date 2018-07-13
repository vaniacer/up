# -*- encoding: utf-8 -*-


def description(args):
	return "\nStop jboss on server {server}\n".format(server=args.server)


def run(args):

	message = {'top': '\n<b>Выполняю jboss.stop</b>\n'.format(wdir=args.wdir), 'bot': ''}
	command = ['ssh', args.server, '{wdir}/krupd jboss.stop'.format(wdir=args.wdir)]
	dick = {'command': command, 'message': message, 'download': ''}

	return dick
