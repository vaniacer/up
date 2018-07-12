# -*- encoding: utf-8 -*-


def description(args):
	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	return "\nCopy updates:\n{updates}\nto server {server}\n".format(updates=updates, server=args.server)


def run(args):

	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	message = {'top': '\n<b>Копирую файл(ы):\n{files}</b>\n'.format(files=updates), 'bot': ''}
	command = ['rsync', '-e', 'ssh', '--progress', '-lzuogthvr']
	command.extend(args.update)
	command.extend(['{addr}:{wdir}/updates/new/'.format(addr=args.server, wdir=args.wdir)])
	dick = {'command': command, 'message': message, 'download': ''}

	return dick
