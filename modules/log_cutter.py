# -*- encoding: utf-8 -*-


def log_cutter(log):

	log = log.decode('utf-8', errors='replace')
	log_size = len(log)
	if log_size > 4000:
		cutted_log = u'{head!s}{first!s}\n...\n{last!s}'.format(
			head='<b>Log is too long to store in history, cutting</b>\n',
			first=log[:2000],
			last=log[-2000:],
		)

		return cutted_log

	return log
