# -*- encoding: utf-8 -*-

from datetime import datetime
from popen_call import my_call, message
from download_upload import download_file


def description(args, log):
	log.write('\nGet current day logs from server:\n%s' % args.server)


def run(args, log):

	filename = '{server}_daylogs_{date:%d-%m-%Y}.zip'.format(server=args.server, date=datetime.now())
	message('\n<b>Копирую файл - {file}</b>\n'.format(file=filename), log)

	download = {
		'file': ['{wdir}/temp/{file}'.format(wdir=args.wdir, file=filename)],
		'kill': True,
		'dest': '',
	}

	command = [
		'ssh', args.server,
		''' find {wdir}/jboss-bas-*/standalone/log -type f -daystart -ctime 0 | xargs zip -jy {file} > /dev/null
			for i in ${{PIPESTATUS[@]}}; {{ ((error+=$i)); }}; exit $error
		'''.format(wdir=args.wdir, file=download['file'][0])
	]

	error = my_call(command, log)
	if error == 0:
		error += download_file(download, args.server, log)

		message(
			""" \n<b>File will be stored until tomorrow, please download it if you need this file!</b>
				\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>\n
			""".format(file=filename), log
		)

	return error
