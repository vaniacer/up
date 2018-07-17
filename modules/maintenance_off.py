# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write('\nStop dummy page on server %s\n' % args.server)


def run(args, log, pid):

	message_top = ['printf', '\n<b>Выключаю страницу "Регламентные работы"</b>\n'.format(wdir=args.wdir)]
	my_popen(message_top, log, pid)

	command = ['ssh', args.server, '~/.utils/dp.sh --stop']
	error = my_popen(command, log, pid)
	return error
