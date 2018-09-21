# -*- encoding: utf-8 -*-

from os import remove
from pg_writer import psql
from popen_call import message


def description(args, log):
	names = '\n'.join(update.split('/')[-1] for update in args.update)
	log.write('\nDelete script(s):\n{updates}\n'.format(updates=names))


def run(args, log):

	sql = ''
	error = 0
	names = '\n'.join(update.split('/')[-1] for update in args.update)
	message('\n<b>Удаляю пакет(ы) обновлений:</b>\n{updates}\n'.format(updates=names), log)

	for update in args.update:
		sql += "delete from ups_update where file = '{update}';".format(update=update)
		try:
			remove(update)
		except OSError:
			error += 1
	error += psql(sql)

	return error
