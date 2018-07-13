# -*- encoding: utf-8 -*-


def description(args):
	return "\nUpdate server {server} with update {update}\n".format(server=args.server, update=args.update[0])


def run(args):

	message = {'top': '\nUnder construction\n', 'bot': ''}
	command = ['echo']
	dick = {'command': command, 'message': message}

	return dick
