# -*- encoding: utf-8 -*-

from up.settings import DUMP_DIR
from subprocess import call
import os


def upload_file(upload, server, log):

	list_of_files = upload['file']
	destination = upload['dest']

	rsync_opt = ['rsync', '--progress', '-lzuogthvr']
	rsync_opt.extend(list_of_files)
	rsync_opt.extend(['{addr}:{dest}/'.format(dest=destination, addr=server)])

	error = call(rsync_opt, stdout=log, stderr=log)
	return error


def download_file(download, server, log):
	"""Закачка файлов."""

	dump_dir = DUMP_DIR
	files = ' '.join(download['file'])

	if download['dest']:
		dump_dir = os.path.join(DUMP_DIR, download['dest'])

	try:
		os.mkdir(dump_dir)
	except OSError:
		pass

	rsync_opt = [
		'rsync', '--progress', '-lzuogthvr',
		'{addr}:{files}'.format(addr=server, files=files), dump_dir,
	]

	if download['kill']:
		rsync_opt.extend(['--remove-source-files'])

	error = call(rsync_opt, stdout=log, stderr=log)
	return error
