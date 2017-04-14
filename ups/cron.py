# -*- encoding: utf-8 -*-

from .commands_engine import add_event, del_job
from django.conf import settings as conf
import os


def get_cron_logs(project):
	"""Создает события в истории на основе логов крона."""

	logfiles = os.listdir(conf.CRON_DIR)
	selected = {'cronjbs': logfiles}

	if logfiles:

		history = project.history_set.order_by('date').reverse()

		for filename in logfiles:
			event = history.filter(cron=str(filename))[0]

			f = open(os.path.join(conf.CRON_DIR, filename), 'r')
			out = f.readlines()
			f.close()

			err = ''.join(out[-1].split()[1:])
			date = ''.join(out[-2].split()[1:])
			del out[-2:]
			out = ''.join(out)

			dick = {'project': event.proj, 'user': event.user, 'cmd': event.name}
			add_event(dick, out, int(err), event.cron, date)
			os.remove(os.path.join(conf.CRON_DIR, filename))

		del_job(selected)
