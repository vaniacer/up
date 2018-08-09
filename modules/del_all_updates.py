# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nDelete all updates from server {server}\n'.format(server=args.server))


def run(args, log):

	message('\n<b>Удаляю все файлы из каталога {wdir}/updates/new</b>\n'.format(wdir=args.wdir), log)
	command = ['ssh', args.server, 'rm {wdir}/updates/new/*'.format(wdir=args.wdir)]
	error = my_call(command, log)
	return error
