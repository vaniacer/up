# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write('\nDelete all updates from server {server}\n'.format(server=args.server))


def run(args, log, pid):

	message_top = ['printf', '\n<b>Удаляю все файлы из каталога {wdir}/updates/new</b>\n'.format(wdir=args.wdir)]
	my_popen(message_top, log, pid)

	command = ['ssh', args.server, 'rm {wdir}/updates/new/*'.format(wdir=args.wdir)]
	error = my_popen(command, log, pid)
	return error
