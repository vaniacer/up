# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	log.write('\nDelete updates:\n{updates}\nfrom server {server}\n'.format(updates=updates, server=args.server))


def run(args, log):

	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	message(
		'\n<b>Удаляю файлы:\n{updates}\nиз каталога {wdir}/updates/new</b>\n'.format(
			updates=updates,
			wdir=args.wdir
		), log
	)

	updates = ' '.join(update.split('/')[-1] for update in args.update)
	command = ['ssh', args.server, 'cd {wdir}/updates/new/; rm {updates}'.format(updates=updates, wdir=args.wdir)]
	error = my_call(command, log)
	return error
