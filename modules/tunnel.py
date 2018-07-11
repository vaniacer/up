# -*- encoding: utf-8 -*-

import socket


def description(server):
	return "\nMake ssh tunnel to bind port of server:\n%s" % server


def run(server, port, wdir):

	timer = 60  # If not used, connection will be dropped after this amount of seconds
	lport = 42250  # default 42250

	command = ['-f', '-L', '0.0.0.0:{lport}:127.0.0.1:{rport}'.format(lport=lport, rport=port), 'sleep', str(timer)]

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	while True:
		error = sock.connect_ex(('127.0.0.1', lport))
		if error == 0:
			break
		lport += 1

	link = ''
	postfixes = ('/application', '/login', '')

	for postfix in postfixes:
		link += '\n<a href="http://__URL__:{lport}{postfix}">http://__URL__:{lport}{postfix}</a>\n'.format(
			lport=lport,
			postfix=postfix,
		)

	message = '\n-----{ <b>Server %s</b> }-----\n%s' % (server, link)
	return command, message
