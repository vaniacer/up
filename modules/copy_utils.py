# -*- encoding: utf-8 -*-

from os.path import expanduser
from popen_call import message
from download_upload import upload_file


def description(args, log):
	log.write('\nCopy utils folder to server {server}\n'.format(server=args.server))


def run(args, log):

	home = expanduser('~')
	message('\n<b>Копирую скрипты</b>\n', log)
	upload = {'file': ['{home}/utils/'.format(home=home)], 'dest': '~/.utils'}
	error = upload_file(upload, args.server, log, limit=args.limit)
	return error
