# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	log.write('\nDelete updates:\n{updates}\nfrom server {server}\n'.format(updates=updates, server=args.server))


def run(args, log, pid):

	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	message_top = ['printf', '\n<b>Удаляю файлы:\n{updates}\nиз каталога {wdir}/updates/new</b>\n'.format(
			updates=updates,
			wdir=args.wdir
		)
	]
	my_popen(message_top, log, pid)

	updates = ' '.join(update.split('/')[-1] for update in args.update)
	command = ['ssh', args.server, 'cd {wdir}/updates/new/; rm {updates}'.format(updates=updates, wdir=args.wdir)]
	error = my_popen(command, log, pid)
	return error
