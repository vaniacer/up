# -*- encoding: utf-8 -*-

from download_upload import upload_file
from popen_call import message


def description(args, log):
	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	log.write('\nCopy updates:\n{updates}\nto server {server}\n'.format(updates=updates, server=args.server))


def run(args, log):

	updates = '\n'.join(update.split('/')[-1] for update in args.update)
	message('\n<b>Копирую файл(ы):\n{files}</b>\n'.format(files=updates), log)
	upload = {'file': args.update, 'dest': '{wdir}/updates/new/'.format(wdir=args.wdir)}
	error = upload_file(upload, args.server, log)
	return error
