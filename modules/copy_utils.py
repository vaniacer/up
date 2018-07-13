# -*- encoding: utf-8 -*-

from os.path import expanduser


def description(args):
	return "\nCopy utils folder to server {server}\n".format(server=args.server)


def run(args):

	home = expanduser('~')
	message = {'top': '\n<b>Копирую скрипты</b>\n', 'bot': ''}
	command = [
		'rsync', '-e', 'ssh', '--progress', '-lzuogthvr', '{home}/utils'.format(home=home),
		'{addr}:~/.utils'.format(addr=args.server),
	]
	dick = {'command': command, 'message': message}

	return dick
