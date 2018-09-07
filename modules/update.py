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
	update = args.update[0]
	log.write('\nUpdate server {server} with update {update}\n'.format(
		update=update.split('/')[-1],
		server=args.server,
	))


def run(args, log):

	error = 0
	update = args.update[0]
	upl_dir = '{wdir}/updates/new'.format(wdir=args.wdir)
	upd_dir = '{wdir}/updates/update'.format(wdir=args.wdir)

	upload = {'file': [update], 'dest': upl_dir}
	error += upload_file(upload, args.server, log)
	if error:
		return error

	update_command = [
		'ssh', args.server,
		''' cd {wdir}
			[[ -d "{updir}" ]] && rm -r "{updir}"
			err_exit () {{ error=$?; printf "$1"; exit $error; }}
			
			printf "\nUnzip files.\n"
			unzip -o {upl_dir}/{file} -d updates > /dev/null \
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
			upl_dir=upl_dir,
			wdir=args.wdir,
			updir=upd_dir,
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
	error += maintenance_on(args, log)
	if error:

		return error

	# Stoping jboss instance
	error += jboss_stop(args, log)
	if error:

		return error

	# Running update
	error += my_call(update_command, log)
	if error:

		return error

	# Starting jboss
	error += jboss_start(args, log)
	if error:

		return error

	# Need make pause
	sleep(10)

	# Running data imports
	error += my_call(import_command, log)
	if error:

		return error

	# Restarting jboss
	error = jboss_restart(args, log)
	if error:

		return error

	# Stop dummy page
	error += maintenance_off(args, log)
	if error:

		return error

	message('\nUpdate complete\n', log)
	return error
