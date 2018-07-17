# -*- encoding: utf-8 -*-

from datetime import datetime
from my_popen import my_popen
from download_upload import download_file


def description(args, log):
	log.write("\nBackup system on server %s" % args.server)


def run(args, log, pid):

	filename = '{server}_system_{date:%d-%m-%Y}.zip'.format(server=args.server, date=datetime.now())
	message_top = ['printf', '\n<b>Копирую файл - {file}</b>\n'.format(file=filename)]
	message_bot = [
		'printf',
		''' \n<b>File will be stored until tomorrow, please download it if you need this file!</b>
			\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>
		'''.format(file=filename)
	]

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'kill': False,
		'dest': '',
	}

	command = [
		'ssh', args.server,
		''' zip -ry {file} \
			{wdir}/jboss-bas-*/standalone/{{configuration,deployments}}/* \
			$(find {wdir} -maxdepth 1 -type f) \
			{wdir}/templates > /dev/null || {{
				error=$?
				printf "<b>Ошибка резервного копирования</b>"
				exit $error
			}}		
		'''.format(wdir=args.wdir, file=download['file'][0])
	]

	my_popen(message_top, log, pid)

	error = my_popen(command, log, pid)
	download_error = download_file(download, args.server, log)
	if download_error > 0:
		error = download_error

	my_popen(message_bot, log, pid)

	return error
