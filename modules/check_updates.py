# -*- encoding: utf-8 -*-


def description(server):
	return "\nShow updates of server:\n%s" % server


def run(server, port, wdir):

	command = ['ls {wdir}/updates/new'.format(wdir=wdir)]
	message = '\n-----{ <b>Server %s</b> }-----\n\nПакеты обновлений:\n' % server

	return command, message

