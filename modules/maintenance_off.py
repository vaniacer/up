# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nStop dummy page on server %s\n' % args.server)


def run(args, log):

	message('\n<b>Выключаю страницу "Регламентные работы"</b>\n'.format(wdir=args.wdir), log)
	command = ['ssh', args.server, '~/.utils/dp.sh --stop']
	error = my_call(command, log)
	return error
