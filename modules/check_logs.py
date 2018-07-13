# -*- encoding: utf-8 -*-


def description(args):
	return "\nShow logs of server:\n%s" % args.server


def run(args):

	command = ['ssh', args.server, 'cat {wdir}/jboss-bas-*/standalone/log/server.log'.format(wdir=args.wdir)]
	message = {'top': '\n-----{ <b>Server %s</b> }-----\n' % args.server, 'bot': ''}
	dick = {'command': command, 'message': message}

	return dick
