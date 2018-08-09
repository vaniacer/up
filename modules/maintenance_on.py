# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nStart dummy page on server %s\n' % args.server)


def run(args, log):

	message('\n<b>Включаю страницу "Регламентные работы"</b>\n'.format(wdir=args.wdir), log)
	command = ['ssh', args.server, '~/.utils/dp.sh --start --jport {port}'.format(port=args.port)]
	error = my_call(command, log)
	return error
