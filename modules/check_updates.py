# -*- encoding: utf-8 -*-


def description(args):
	return "\nShow updates of server:\n%s" % args.server


def run(args):

	command = ['ls {wdir}/updates/new'.format(wdir=args.wdir)]
	message = '\n-----{ <b>Server %s</b> }-----\n\nПакеты обновлений:\n' % args.server

	dick = {'command': command, 'message': message, 'download': ''}

	return dick

