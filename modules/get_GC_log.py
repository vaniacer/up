# -*- encoding: utf-8 -*-

from datetime import datetime
from popen_call import my_call, message
from download_upload import download_file


def description(args, log):
	log.write('\nGet GC log from server:\n%s' % args.server)


def run(args, log):

	filename = 'gc.log'
	message('\n<b>Копирую файл - {file}</b>\n'.format(file=filename), log)

	download = {
		'file': ['{wdir}/jboss-bas-*/standalone/log/gc.log'.format(wdir=args.wdir, file=filename)],
		'kill': True,
		'dest': '',
	}

	error = download_file(download, args.server, log)

	message(
		""" \n<b>File will be stored until tomorrow, please download it if you need this file!</b>
			\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>\n
		""".format(file=filename), log
	)

	return error
