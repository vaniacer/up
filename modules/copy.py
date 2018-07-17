# -*- encoding: utf-8 -*-

from download_upload import upload_file
from my_popen import my_popen


def description(args, log):
	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	log.write('\nCopy updates:\n{updates}\nto server {server}\n'.format(updates=updates, server=args.server))


def run(args, log, pid):

	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	message_top = ['printf', '\n<b>Копирую файл(ы):\n{files}</b>\n'.format(files=updates)]

	my_popen(message_top, log, pid)

	upload = {'file': args.update, 'dest': '{wdir}/updates/new/'.format(wdir=args.wdir)}
	error = upload_file(upload, args.server, log)
	return error
