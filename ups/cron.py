# -*- encoding: utf-8 -*-

from django.shortcuts import get_object_or_404
from .commands import add_event, get_key
from django.conf import settings as conf
from .commands import del_job
from .models import Job
import os


def get_cron_logs():
	"""Создает события в истории на основе логов крона."""
	logfiles = os.listdir(conf.CRON_DIR)

	if logfiles:
		for filename in logfiles:
			job = get_object_or_404(Job, cron=filename)

			f = open(os.path.join(conf.CRON_DIR, filename), 'r')
			out = f.readlines()
			f.close()

			err = ''.join(out[-2].split()[1:])
			dat = ' '.join(out[-1].split()[1:])
			out = ''.join(out[:-2])

			try:
				err = int(err)
			except ValueError:
				continue

			dick = {
				'desc': out,
				'cdat': dat,
				'exit': err,
				'serv': job.serv,
				'cron': filename,

				'name': job.name,
				'user': job.user,
				'proj': job.proj,
				'uniq': get_key(),
			}

			os.remove(os.path.join(conf.CRON_DIR, filename))
			add_event(dick)

			if not job.perm:  # удаляю если задача не постоянная
				del_job(filename)

