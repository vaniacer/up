# -*- encoding: utf-8 -*-


def description(server):
	return "\nShow logs of server:\n%s" % server


def run(server, port, wdir):

	command = ['cat {wdir}/jboss-bas-*/standalone/log/server.log'.format(wdir=wdir)]
	message = '\n-----{ <b>Server %s</b> }-----\n' % server

	return command, message

