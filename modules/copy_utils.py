# -*- encoding: utf-8 -*-

from os.path import expanduser
from download_upload import upload_file
from my_popen import my_popen


def description(args, log):
	log.write('\nCopy utils folder to server {server}\n'.format(server=args.server))


def run(args, log, pid):

	home = expanduser('~')
	message_top = ['printf', '\n<b>Копирую скрипты</b>\n']

	my_popen(message_top, log, pid)
	upload = {'file': ['{home}/utils/'.format(home=home)], 'dest': '~/.utils'}
	error = upload_file(upload, args.server, log)
	return error
