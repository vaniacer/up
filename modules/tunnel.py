# -*- encoding: utf-8 -*-

import socket


def description(server):
	return "\nMake ssh tunnel to bind port of server:\n%s" % server


def run(server, port, wdir):

	timer = 60  # If not used, connection will be dropped after this amount of seconds
	lport = 42250  # default 42250

	while True:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ptest = sock.connect_ex(('127.0.0.1', lport))
		sock.close()
		if ptest:
			break
		lport += 1

	link = ''
	postfixes = ('/application', '/login', '')

	command = ['-f', '-L', '0.0.0.0:{lport}:127.0.0.1:{rport}'.format(lport=lport, rport=port), 'sleep', str(timer)]

	for postfix in postfixes:
		link += '\n<a href="http://__URL__:{lport}{postfix}">http://__URL__:{lport}{postfix}</a>\n'.format(
			lport=lport,
			postfix=postfix,
		)

	message = '\n-----{{ <b>Server {server}</b> }}-----\n{link}'.format(server=server, link=link)
	return command, message
