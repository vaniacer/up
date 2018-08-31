# -*- encoding: utf-8 -*-

from django.shortcuts import get_object_or_404
from modules.log_cutter import log_cutter
from .commands import add_event, get_key
from django.conf import settings as conf
from os.path import join as opj
from os import listdir, remove
from .commands import del_job
from .models import Job


def get_cron_logs():
	"""Создает события в истории на основе логов крона."""
	logfiles = listdir(conf.CRON_DIR)

	if logfiles:
		for filename in logfiles:
			job = get_object_or_404(Job, cron=filename)

			with open(opj(conf.CRON_DIR, filename)) as f:
				out = f.readlines()

			dat = ' '.join(out[-1].split()[1:])
			err = ''.join(out[-2].split()[1:])
			out = ''.join(out[:-2])
			log = log_cutter(out)

			try:
				err = int(err)
			except ValueError:
				continue

			dick = {
				'desc': log,
				'cdat': dat,
				'exit': err,
				'serv': job.serv,
				'cron': filename,
				'name': job.name,
				'user': job.user,
				'proj': job.proj,
				'uniq': get_key(),
			}

			remove(opj(conf.CRON_DIR, filename))
			add_event(dick)

			if not job.perm:  # удаляю если задача не постоянная
				del_job(filename)
