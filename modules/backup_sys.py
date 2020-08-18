# -*- encoding: utf-8 -*-

from download_upload import download_file
from popen_call import my_call, message
from datetime import datetime


def description(args, log):
	log.write("\nBackup system on server %s" % args.server)


def run(args, log):

	error = 0
	filename = '{server}_system_{date:%d-%m-%Y}.zip'.format(server=args.server, date=datetime.now())
	message('\n<b>Копирую файл {file}</b>\n'.format(file=filename), log)

	download = {'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)], 'dest': ''}
	command = [
		'ssh', args.server,
		''' zip -ry {file} \
			{wdir}/jboss-bas-*/standalone/{{configuration,deployments}}/* \
			$(find {wdir} -maxdepth 1 -type f) \
			{wdir}/templates > /dev/null
		'''.format(wdir=args.wdir, file=download['file'][0])
	]

	error += my_call(command, log)
	if error == 0:
		error += download_file(download, args.server, log, link=True, limit=args.limit)

	return error
