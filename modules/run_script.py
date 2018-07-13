# -*- encoding: utf-8 -*-

import os
from up.settings import DUMP_DIR


def description(args):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	return "\nRun script(s):\n{scripts}\non server {server}\n".format(scripts=scripts, server=args.server)


def run(args):

	filename = args.dump[0]
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	message = {'top': '\n<b>Копирую файл(ы):\n{}</b>\n'.format(scripts), 'bot': ''}
	upload = {'file': args.script, 'dest': tmp_dir}
	command = [
		'ssh', args.server,
		'''
		echo
		'''.format(file=filename, wdir=args.wdir, tmp=tmp_dir)
	]

	dick = {'command': command, 'message': message, 'upload': upload}

	return dick
