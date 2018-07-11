# -*- encoding: utf-8 -*-


def description(args):
	return "\nShow logs of server:\n%s" % args.server


def run(args):

	command = ['cat {wdir}/jboss-bas-*/standalone/log/server.log'.format(wdir=args.wdir)]
	message = '\n-----{ <b>Server %s</b> }-----\n' % args.server

	return command, message

