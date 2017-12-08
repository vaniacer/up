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

		i = 0
		dumplist = []

		for dump in dumps:
			i += 1
			dumplist.extend([{'id': i, 'name': dump, 'size': os.stat(os.path.join(path, dump)).st_size}])

		return dumplist
