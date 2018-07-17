# -*- encoding: utf-8 -*-

from datetime import datetime
from my_popen import my_popen
from download_upload import download_file


def description(args, log):
	log.write('\nGet all logs from server:\n%s' % args.server)


def run(args, log, pid):

	filename = '{server}_allogs_{date:%d-%m-%Y}.zip'.format(server=args.server, date=datetime.now())
	message_top = ['printf', '\n<b>Копирую файл - {file}</b>\n'.format(file=filename)]
	message_bot = [
		'printf',
		""" \n<b>File will be stored until tomorrow, please download it if you need this file!</b>
			\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>\n
		""".format(file=filename),
	]

	download = {
		'file': ['{wdir}/temp/{file}'.format(wdir=args.wdir, file=filename)],
		'kill': True,
		'dest': '',
	}

	command = [
		'ssh', args.server,
		'zip -jy {file} {wdir}/jboss-bas-*/standalone/log/* > /dev/null'.format(
			wdir=args.wdir,
			file=download['file'][0]
		)
	]

	my_popen(message_top, log, pid)

	error = my_popen(command, log, pid)
	download_error = download_file(download, args.server, log)
	if download_error > 0:
		error = download_error

	my_popen(message_bot, log, pid)
	return error
