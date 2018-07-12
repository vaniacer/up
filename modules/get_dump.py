# -*- encoding: utf-8 -*-

from datetime import datetime
from .backup_db import command_template as db_bkp_command_template


def description(args):
	return "\nGet database dump from server:\n%s" % args.server


def run(args):

	filename = '{server}_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message = {
		'top': '\n<b>Копирую дамп: {file}</b>\n'.format(file=filename),
		'bot':
			"""
			\n<b>Files will be stored until tomorrow, please download them if you needed!</b>
			\n<a class='btn btn-primary' href='/download_dump/{pro}/{file}'>Download</a>
			""".format(file=filename, pro=args.proid),
	}

	download = {
		'file': ['{wdir}/backup/{file}'.format(wdir=args.wdir, file=filename)],
		'dest': args.proname,
		'kill': True,
	}

	command = ['ssh', args.server, db_bkp_command_template.format(wdir=args.wdir, file=download['file'][0])]
	dick = {'command': command, 'message': message, 'download': download}

	return dick
