# -*- encoding: utf-8 -*-

from os.path import isfile, splitext, basename
from up.settings import DUMP_DIR
from os.path import join as opj
from popen_call import message
from modules.uniq import uniq
from subprocess import call
from conf import rslimit


def upload_file(upload, server, log, kill=False, limit=0):
	"""Закачка файлов на сервер, опции:
		kill=False - удалить источник если True
		limit=0 - макс. скорость закачки для rsync в kb, 0 - без ограничений"""
	files = upload['file']
	if not files:
		message('\n<b>Файлы не найдены!</b>\n', log)
		return 1

	destination = upload['dest']
	rsync_opt = ['rsync', '--progress', '-gzort']
	if kill:
		rsync_opt.extend(['--remove-source-files'])
	if int(limit):
		rsync_opt.extend(['--bwlimit={}'.format(limit)])
	elif rslimit:
		rsync_opt.extend(['--bwlimit={}'.format(rslimit)])
	rsync_opt.extend(files)
	rsync_opt.extend(['{addr}:{dest}/'.format(dest=destination, addr=server)])

	error = call(rsync_opt, stdout=log, stderr=log)
	return error


def download_file(download, server, log, kill=False, link=False, silent=False, limit=0):
	"""Закачка файлов с сервера, опции:
		link=False - добавить ссылку на закачку с UpS'а если True
		kill=False - удалить источник если True
		silent=False - не выводить % загрузки если True
		limit=0 - макс. скорость закачки для rsync в kb, 0 - без ограничений"""
	error = 0
	dump_dir = DUMP_DIR
	if download['dest']:
		dump_dir = opj(DUMP_DIR, download['dest'])

	for remote_file in download['file']:

		filename = basename(remote_file)
		destination = opj(dump_dir, filename)

		if isfile(destination):
			filename, extension = splitext(filename)
			filename = '{old}_{key}{ext}'.format(old=filename, key=uniq(), ext=extension)
			destination = opj(dump_dir, filename)

		rsync_opt = ['rsync', '-gzort', '--progress', '{S}:{F}'.format(S=server, F=remote_file), destination]
		if silent:
			rsync_opt.extend(['--quiet'])
		if kill:
			rsync_opt.extend(['--remove-source-files'])
		if int(limit):
			rsync_opt.extend(['--bwlimit={}'.format(limit)])
		elif rslimit:
			rsync_opt.extend(['--bwlimit={}'.format(rslimit)])

		new_error = call(rsync_opt, stdout=log, stderr=log)
		if new_error == 0 and link:
			download_link = "<a class='btn btn-primary' href='/dumps/{F}'>Download {F}</a>\n".format(F=filename)
			message("\n<b>File will be stored until tomorrow, download it please if you need!</b>\n{L}\n".format(
				L=download_link), log
			)
		else:
			error = error + new_error

	return error
