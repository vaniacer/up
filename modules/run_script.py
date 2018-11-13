# -*- encoding: utf-8 -*-

from download_upload import upload_file
from popen_call import my_call, message
from os.path import expanduser


def description(args, log):
	scripts = '\n'.join(script.split('/')[-1] for script in args.script)
	log.write('\nRun script(s):\n{scripts}\non server {server}\n'.format(scripts=scripts, server=args.server))


def check_opt(opt):
	if opt:
		return '<b>Параметры:\n</b>{}\n'.format(opt)
	return ''


def run(args, log):

	error = 0
	updates = None
	home = expanduser('~')
	upd_dir = '{wdir}/updates/new'.format(wdir=args.wdir)
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)

	# remove .yml and .sql from upload list
	files_to_upload = [script for script in args.script if '.sql' not in script and '.yml' not in script]
	if files_to_upload:
		message('\n<b>Копирую файл(ы):</b>\n', log)
		upload = {'file': files_to_upload, 'dest': tmp_dir}
		error += upload_file(upload, args.server, log)

	if args.update:
		upload = {'file': args.update, 'dest': upd_dir}
		updates = ['{dir}/{upd}'.format(dir=upd_dir, upd=update.split('/')[-1]) for update in args.update]
		error += upload_file(upload, args.server, log)

	for script, options in zip(args.script, args.options):

		with open(script) as f:
			body = f.read()

		filename = script.split('/')[-1]
		script_type = script.split('.')[-1]
		filepath = '{tmp}/{file}'.format(tmp=tmp_dir, file=filename)
		message('\n<b>Выполняю скрипт {file}, тело скрипта:</b>\n<i>{body}</i>\n{opts}\n<b>Результат:</b>\n'.format(
			opts=check_opt(options),
			file=filename,
			body=body,
		), log)

		if updates:
			options += ' '.join(updates)

		# ------------------{ Run bash script }--------------------------------
		if script_type == 'sh':
			command = [
				'ssh', args.server, 'cd {wdir}; bash {file} {options}'.format(
					options=options,
					wdir=args.wdir,
					file=filepath,
				)
			]
			error += my_call(command, log)

		# ------------------{ Run python script }------------------------------
		elif script_type == 'py':
			command = [
				'ssh', args.server, 'cd {wdir}; python {file} {options}'.format(
					options=options,
					wdir=args.wdir,
					file=filepath,
				)
			]
			error += my_call(command, log)

		# ------------------{ Run YML script }---------------------------------
		elif script_type == 'yml':
			command = [
				'ansible-playbook', script, '-i', '%s,' % args.server,
				'--vault-password-file', '%s/vault.txt' % home, '--syntax-check'
			]
			syntax_check = my_call(command, log)
			if syntax_check == 0:
				error += my_call(command[0:-1], log)  # run without '--syntax-check'

		# ------------------{ Unknown script type }----------------------------
		else:
			message('\nUnknown script type.\n', log)
			error += 1

	remove_tmp = ['ssh', args.server, 'rm -rf {tmp}'.format(tmp=tmp_dir)]
	my_call(remove_tmp, log)
	return error
