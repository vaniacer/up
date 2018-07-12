# -*- encoding: utf-8 -*-


def description(args):
	return "\nDelete all updates from server {server}\n".format(server=args.server)


def run(args):

	message = {'top': '\n<b>Удаляю все файлы из каталога {wdir}/updates/new</b>\n'.format(wdir=args.wdir), 'bot': ''}
	command = ['ssh', args.server, 'rm {wdir}/updates/new/*'.format(wdir=args.wdir)]
	dick = {'command': command, 'message': message, 'download': ''}

	return dick
