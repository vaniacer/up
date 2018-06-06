# -*- encoding: utf-8 -*-

from .commands_engine import add_event, del_job, get_key
from django.conf import settings as conf
from .models import Job
import os


def get_cron_logs():
	"""Создает события в истории на основе логов крона."""
	logfiles = os.listdir(conf.CRON_DIR)

	if logfiles:
		for filename in logfiles:
			job = Job.objects.get(cron=filename)
			srv = job.serv

			f = open(os.path.join(conf.CRON_DIR, filename), 'r')
			out = f.readlines()
			f.close()

			err = ''.join(out[-2].split()[1:])
			dat = ' '.join(out[-1].split()[1:])
			out = ''.join(out[:-2])

			dick = {'project': job.proj, 'user': job.user, 'name': job.name}
			os.remove(os.path.join(conf.CRON_DIR, filename))
			add_event(dick, out, int(err), filename, get_key(), dat, srv)

			if not job.perm:  # удаляю если задача не постоянная
				del_job(filename)
