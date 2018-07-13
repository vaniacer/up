# -*- encoding: utf-8 -*-

from datetime import datetime


command_template = '''
		find {wdir}/jboss-bas-*/standalone/log -type f -daystart -ctime 0 | xargs zip -jy {file} > /dev/null
	'''


def description(args):
	return "\nGet current day logs from server:\n%s" % args.server


def run(args):

	filename = '{server}_daylogs_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message = {
		'top': '\n<b>Копирую файл - {file}</b>\n'.format(file=filename),
		'bot':
			"""
			\n<b>File will be stored until tomorrow, please download it if you need this file!</b>
			\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>\n
			""".format(file=filename),
	}

	download = {
		'file': ['{wdir}/temp/{file}'.format(wdir=args.wdir, file=filename)],
		'kill': True,
		'dest': '',
	}

	command = ['ssh', args.server, command_template.format(wdir=args.wdir, file=download['file'][0])]
	dick = {'command': command, 'message': message, 'download': download}

	return dick
