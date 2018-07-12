# -*- encoding: utf-8 -*-

from datetime import datetime
from .backup_db import command_template as db_bkp_command_template
from .backup_sys import command_template as sys_bkp_command_template


def description(args):
	return "\nBackup database and system on server:\n%s" % args.server


def run(args):

	sys_filename = '{server}_system_{date:%d-%m-%Y}.zip'.format(server=args.server, date=datetime.now())
	db_filename = '{server}_dbdump_{date:%d-%m-%Y}.gz'.format(server=args.server, date=datetime.now())
	message = {
		'top': '\n<b>Копирую файлы: {dbfile}, {sysfile}</b>\n'.format(dbfile=db_filename, sysfile=sys_filename),
		'bot':
			"""
			\n<b>Files will be stored until tomorrow, please download them if you needed!</b>
			\n<a class='btn btn-primary' href='/dumps/{dbfile}'>Download dbdump</a>
			\n<a class='btn btn-primary' href='/dumps/{sysfile}'>Download sysarch</a>\n
			""".format(dbfile=db_filename, sysfile=sys_filename),
	}

	db_file = '{wdir}/backup/{file}'.format(wdir=args.wdir, file=db_filename)
	sys_file = '{wdir}/backup/{file}'.format(wdir=args.wdir, file=sys_filename)

	download = {
		'file': [db_file, sys_file],
		'dest': '',
	}

	command = [
		'ssh', args.server,
		db_bkp_command_template.format(wdir=args.wdir, file=download['file'][0]),
		sys_bkp_command_template.format(wdir=args.wdir, file=download['file'][1]),
	]

	dick = {'command': command, 'message': message, 'download': download}

	return dick
