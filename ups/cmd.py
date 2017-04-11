# -*- encoding: utf-8 -*-

from .buttons import cron_job, select_logs, select_job_del, select_ls, run_now


commands = {
	'RUN': {'cmd': run_now, 'url': ''},
	'CRON': {'cmd': cron_job, 'url': ''},
	'select_ls': {'cmd': select_ls, 'url': ''},
	'select_logs': {'cmd': select_logs, 'url': ''},
	'select_job_del': {'cmd': select_job_del, 'url': '#cron'},
}
