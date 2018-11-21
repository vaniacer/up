# -*- encoding: utf-8 -*-

from up.settings import DUMP_DIR
from os.path import join as opj
from popen_call import message
from subprocess import call


def upload_file(upload, server, log):

	files = upload['file']
	if not files:
		message('\n<b>Файлы не найдены!</b>\n', log)
		return 1

	destination = upload['dest']
	rsync_opt = ['rsync', '--progress', '-lzuogthvr']
	rsync_opt.extend(files)
	rsync_opt.extend(['{addr}:{dest}/'.format(dest=destination, addr=server)])

	error = call(rsync_opt, stdout=log, stderr=log)
	return error


def download_file(download, server, log):
	"""Закачка файлов."""

	files = ' '.join(download['file'])
	if not files:
		message('\n<b>Файлы не найдены!</b>\n', log)
		return 1

	dump_dir = DUMP_DIR
	if download['dest']:
		dump_dir = opj(DUMP_DIR, download['dest'])

	rsync_opt = [
		'rsync', '--progress', '-lzuogthvr',
		'{addr}:{files}'.format(addr=server, files=files), dump_dir,
	]

	if download['kill']:
		rsync_opt.extend(['--remove-source-files'])

	error = call(rsync_opt, stdout=log, stderr=log)
	return error
