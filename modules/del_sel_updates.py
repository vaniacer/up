# -*- encoding: utf-8 -*-


def description(args):
	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	return "\nDelete updates:\n{updates}\nfrom server {server}\n".format(updates=updates, server=args.server)


def run(args):

	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	message = {
		'top': '\n<b>Удаляю файлы:\n{updates}\nиз каталога {wdir}/updates/new</b>\n'.format(
			updates=updates,
			wdir=args.wdir
		),
		'bot': '',
	}

	updates = ' '.join(update.split('/')[-1] for update in args.update)
	command = ['ssh', args.server, 'cd {wdir}/updates/new/; rm {updates}'.format(updates=updates, wdir=args.wdir)]
	dick = {'command': command, 'message': message, 'download': ''}

	return dick
