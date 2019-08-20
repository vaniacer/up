# -*- encoding: utf-8 -*-

from os.path import isfile, splitext, basename
from up.settings import DUMP_DIR
from os.path import join as opj
from popen_call import message
from modules.uniq import uniq
from subprocess import call


def upload_file(upload, server, log, kill=False):

	files = upload['file']
	if not files:
		message('\n<b>Файлы не найдены!</b>\n', log)
		return 1

	destination = upload['dest']
	rsync_opt = ['rsync', '--progress', '-gzort']
	rsync_opt.extend(files)
	rsync_opt.extend(['{addr}:{dest}/'.format(dest=destination, addr=server)])
	if kill:
		rsync_opt.extend(['--remove-source-files'])

	error = call(rsync_opt, stdout=log, stderr=log)
	return error


def download_file(download, server, log, link=False, silent=False):
	"""Закачка файлов."""

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

		rsync_opt = ['rsync', '--progress', '-gzort', '{S}:{F}'.format(S=server, F=remote_file), destination]

		if download['kill']:
			rsync_opt.extend(['--remove-source-files'])

		if silent:
			rsync_opt.extend(['--quiet'])

		new_error = call(rsync_opt, stdout=log, stderr=log)
		if new_error == 0 and link:
			download_link = "<a class='btn btn-primary' href='/dumps/{F}'>Download {F}</a>\n".format(F=filename)
			message("\n<b>File will be stored until tomorrow, download it please if you need!</b>\n{L}\n".format(
				L=download_link), log
			)
		else:
			error = error + new_error

	return error
