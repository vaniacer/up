# -*- encoding: utf-8 -*-

from maintenance_off import run as maintenance_off
from maintenance_on import run as maintenance_on
from restart import run as jboss_restart
from download_upload import upload_file
from start import run as jboss_start
from stop import run as jboss_stop
from popen_call import my_call
from popen_call import message
from time import sleep


def description(args, log):
	update = args.update[:1]
	log.write('\nUpdate server {server} with update {update}\n'.format(
		update=update.split('/')[-1],
		server=args.server,
	))


def run(args, log):

	error = 0
	update = args.update[:1]
	upd_dir = '{wdir}/updates/update'.format(wdir=args.wdir)
	tmp_dir = '{wdir}/temp/{key}'.format(wdir=args.wdir, key=args.key)

	upload = {'file': update, 'dest': tmp_dir}
	up_error = upload_file(upload, args.server, log)
	if up_error > 0:
		return up_error

	update_command = [
		'ssh', args.server,
		''' cd {wdir}
			[[ -d {updir} ]] && rm -r {updir}
			err_exit () {{ error=$?; printf "$1"; exit $error; }}
			
			printf "\nUnzip files.\n"
			unzip -o {tmp}/{file} -d updates > /dev/null \
				|| err_exit '\nОшибка извлечения файлов из архива!\n'
	
			printf "\nCopy files.\n"
			cp updates/update/*.{{ear,war}} jboss-bas-*/standalone/deployments \
				|| err_exit '\nОшибка копирования файлов для деплоя!\n'
				
			cp -r updates/update/templates/* templates \
				|| err_exit '\nОшибка копирования шаблонов!\n'
				
			rm -r expimp/*
			cp -r updates/update/expimp/* expimp \
				|| err_exit '\nОшибка копирования файлов импорта!\n'
				
			rm -r expimp/config/*
			
			cp updates/update/expimp/config/system_params.list.txt . \
				|| err_exit '\nОшибка копирования!\n'
		
		'''.format(
			file=update.split('/')[-1],
			wdir=args.wdir,
			updir=upd_dir,
			tmp=tmp_dir,
		)
	]

	import_command = [
		'ssh', args.server,
		''' cd {wdir}
			printf "\nImport:\n\n1. DataCreator.\n"
			./DataCreatorUpdate.sh \
				|| err_exit '\nОшибка обновления метаданных!\n'
			
			printf "\n2. Import central.\n"
			./import_ByUUID_Central.sh \
				|| err_exit '\nОшибка импорта!\n'

		'''.format(
			wdir=args.wdir,
		)
	]

	# Start dummy page
	m_error = maintenance_on(args, log)
	if m_error > 0:
		error = m_error

	# Stoping jboss instance
	stop_error = jboss_stop(args, log)
	if stop_error > 0:
		error = stop_error

	# Running update
	cmd1_error = my_call(update_command, log)
	if cmd1_error > 0:
		error = cmd1_error

	# Starting jboss
	start_error = jboss_start(args, log)
	if start_error > 0:
		error = start_error

	# Need make pause
	sleep(10)

	# Running data imports
	cmd2_error = my_call(import_command, log)
	if cmd2_error > 0:
		error = cmd2_error

	# Restarting jboss
	restart_error = jboss_restart(args, log)
	if restart_error > 0:
		error = restart_error

	# Stop dummy page
	m_error = maintenance_off(args, log)
	if m_error > 0:
		error = m_error

	remove_tmp = ['ssh', args.server, 'rm -rf {tmp} {updir}'.format(tmp=tmp_dir, updir=upd_dir)]
	my_call(remove_tmp, log)

	message('\nUpdate complete\n', log)

	return error
