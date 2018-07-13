# -*- encoding: utf-8 -*-


def description(args):
	return "\nStop dummy page on server {server}\n".format(server=args.server)


def run(args):

	message = {'top': '\n<b>Выполняю jboss.start</b>\n'.format(wdir=args.wdir), 'bot': ''}
	command = ['ssh', args.server, '~/.utils/dp.sh --stop']
	dick = {'command': command, 'message': message, 'download': ''}

	return dick
