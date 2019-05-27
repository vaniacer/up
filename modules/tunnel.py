# -*- encoding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from popen_call import my_call


def description(args, log):
	log.write("\nMake ssh tunnel to bind port of server %s" % args.server)


def run(args, log):

	timer = 60     # If not used, connection will be dropped after this amount of seconds
	lport = 42250  # default 42250

	for i in range(42250, 42300):
		lport = i
		sock = socket(AF_INET, SOCK_STREAM)
		ptest = sock.connect_ex(('127.0.0.1', lport))
		sock.close()
		if ptest:
			break

	link = ''
	postfixes = ('/application', '/login', '')
	for postfix in postfixes:
		link += '\n<a target="_blank" href="{url}:{port}{post}">https://{url}:{port}{post}</a>\n'.format(
			url=args.url,
			post=postfix,
			port=lport,
		)

	command2 = [
		'ssh', args.server, '-f', '-L', '0.0.0.0:{LP}:127.0.0.1:{RP}'.format(LP=lport, RP=args.port),
		'sleep', str(timer)
	]

	error = my_call(command2, log)
	if not error:
		log.write(link)

	return error
