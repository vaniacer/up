# -*- encoding: utf-8 -*-


def description(args):
	return "\nStart dummy page on server {server}\n".format(server=args.server)


def run(args):

	message = {'top': '\n<b>Выполняю jboss.start</b>\n'.format(wdir=args.wdir), 'bot': ''}
	command = ['ssh', args.server, '~/.utils/dp.sh --start --jport {port}'.format(port=args.port)]
	dick = {'command': command, 'message': message}

	return dick
