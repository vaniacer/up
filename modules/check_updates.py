# -*- encoding: utf-8 -*-


def description(args):
	return "\nShow updates of server:\n%s" % args.server


def run(args):

	command = ['ssh', args.server, 'ls {wdir}/updates/new'.format(wdir=args.wdir)]
	message = {'top': '\n-----{ <b>Server %s</b> }-----\n\nПакеты обновлений:\n' % args.server, 'bot': ''}
	dick = {'command': command, 'message': message, 'download': ''}

	return dick

