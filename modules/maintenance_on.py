# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write('\nStart dummy page on server %s\n' % args.server)


def run(args, log, pid):

	message_top = ['printf', '\n<b>Включаю страницу "Регламентные работы"</b>\n'.format(wdir=args.wdir)]
	my_popen(message_top, log, pid)

	command = ['ssh', args.server, '~/.utils/dp.sh --start --jport {port}'.format(port=args.port)]
	error = my_popen(command, log, pid)
	return error
