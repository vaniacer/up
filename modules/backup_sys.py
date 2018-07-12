# -*- encoding: utf-8 -*-

from datetime import datetime


command_template = '''
		zip -ry {file} \
		{wdir}/jboss-bas-*/standalone/{{configuration,deployments}}/* \
		$(find {wdir} -maxdepth 1 -type f) \
		{wdir}/templates > /dev/null || {{
			error=$?
			printf "<b>Ошибка резервного копирования</b>"
			exit $error
		}}		
	'''


def description(args):
	return "\nBackup system on server:\n%s" % args.server


def run(args):

	filename = '{server}_system_{date:%d-%m-%Y}.zip'.format(server=args.server, date=datetime.now())
	message = {
		'top': '\n<b>Копирую файл - {file}</b>\n'.format(file=filename),
		'bot':
			"""
			\n<b>File will be stored until tomorrow, please download it if you need this file!</b>
			\n<a class='btn btn-primary' href='/dumps/{file}'>Download</a>\n
			""".format(file=filename),
	}

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'dest': '',
	}

	command = ['ssh', args.server, command_template.format(wdir=args.wdir, file=download['file'][0])]
	dick = {'command': command, 'message': message, 'download': download}

	return dick

