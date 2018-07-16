# -*- encoding: utf-8 -*-

import os
from up.settings import DUMP_DIR


def description(args):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	return "\nRun script(s):\n{scripts}\non server {server}\n".format(scripts=scripts, server=args.server)


def run(args):

	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	message = {'top': '\n<b>Копирую файл(ы):\n{}</b>\n'.format(scripts), 'bot': ''}
	upload = {'file': args.script, 'dest': tmp_dir}

	# Make command from script list
	script_list = ''
	for script in args.script:
		filename = script.split('/')[-1]
		script_type = script.split('.')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		script_list += 'printf "\n<b>Выполняю скрипт {file}</b>\n";'.format(file=filename)

		if script_type == 'sh':
			script_list += 'bash {file};'.format(file=filepath)

		if script_type == 'py':
			script_list += 'python {file};'.format(file=filepath)

	script_list += 'rm -r {tmp}'.format(tmp=tmp_dir)

	command = ['ssh', args.server, script_list]

	dick = {'command': command, 'message': message, 'upload': upload}

	return dick
