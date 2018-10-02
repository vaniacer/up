# -*- encoding: utf-8 -*-

from conf import logsize

halfsize = logsize / 2


def log_cutter(log):

	log = log.decode('utf-8', errors='replace')
	log_size = len(log)
	if log_size > logsize:
		cutted_log = u'{head!s}{first!s}\n...\n{last!s}'.format(
			head='<b>Log is too long to store in history, cutting</b>\n',
			first=log[:halfsize],
			last=log[-halfsize:],
		)

		return cutted_log

	return log
