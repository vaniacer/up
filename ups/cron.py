# -*- encoding: utf-8 -*-

from .commands_engine import add_event, del_job
from django.conf import settings as conf
from .models import Job
import os


def get_cron_logs():
	"""Создает события в истории на основе логов крона."""

	logfiles = os.listdir(conf.CRON_DIR)
	selected = {'cronjbs': logfiles}

	if logfiles:
		for filename in logfiles:
			job = Job.objects.get(cron=filename)

			f = open(os.path.join(conf.CRON_DIR, filename), 'r')
			out = f.readlines()
			f.close()

			err = ''.join(out[-1].split()[1:])
			dat = ''.join(out[-2].split()[1:])
			out = ''.join(out[:-2])

			dick = {'project': job.proj, 'user': job.user, 'cmd': job.name}
			add_event(dick, out, int(err), filename, dat)
			os.remove(os.path.join(conf.CRON_DIR, filename))

		del_job(selected)
