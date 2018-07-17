# -*- encoding: utf-8 -*-

import os
from os.path import expanduser
from up.settings import DUMP_DIR


def description(args):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	return "\nRun script(s):\n{scripts}\non server {server}\n".format(scripts=scripts, server=args.server)


def run(args):

	home = expanduser('~')
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	message = {'top': '\n<b>Копирую файл(ы):\n{}</b>\n'.format(scripts), 'bot': ''}
	upload = {'file': args.script, 'dest': tmp_dir}

	# Make command from script list
	sh_py_sql_script_list = ''
	yml_script_list = []
	ansible_command = []
	yml_command1 = ['ansible-playbook', '--vault-password-file', '%s/vault.txt' % home, '--syntax-check']
	yml_command2 = ['ansible-playbook', '--vault-password-file', '%s/vault.txt' % home, '-i', args.server]

	for script in args.script:
		filename = script.split('/')[-1]
		script_type = script.split('.')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		sh_py_sql_script_list += 'printf "\n<b>Выполняю скрипт {file}</b>\n"; '.format(file=filename)

		if script_type == 'sh':
			sh_py_sql_script_list += 'bash {file}; '.format(file=filepath)
		elif script_type == 'py':
			sh_py_sql_script_list += 'python {file}; '.format(file=filepath)
		elif script_type == 'yml':
			yml_script_list.append(script)

	sh_py_sql_script_list += 'rm -r {tmp}'.format(tmp=tmp_dir)

	command = ['ssh', args.server, sh_py_sql_script_list]

	dick = {'command': command, 'message': message, 'upload': upload}

	return dick
