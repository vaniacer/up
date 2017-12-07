# -*- encoding: utf-8 -*-

from django.conf import settings as conf
import os


def get_dumps(pname):
	"""Создает список дампов."""
	path = os.path.join(conf.MEDIA_ROOT, 'dumps', pname)
	try:  # make project subdir
		os.mkdir(path)
	except OSError:
		pass

	dumps = os.listdir(path)

	if dumps:
		dumplist = [{'name': dump, 'size': os.stat(os.path.join(path, dump)).st_size} for dump in dumps]

		return dumplist
