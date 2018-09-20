# -*- encoding: utf-8 -*-

from os import remove
from pg_writer import psql
from popen_call import message


def description(args, log):
	names = '\n'.join(script.split('/')[-1] for script in args.script)
	log.write('\nDelete script(s):\n{scripts}\n'.format(scripts=names))


def run(args, log):

	error = 0
	names = '\n'.join(script.split('/')[-1] for script in args.script)
	message('\n<b>Удаляю скрипт(ы):</b>\n{scripts}\n'.format(scripts=names), log)

	for script in args.script:
		error += psql("delete from ups_script where file = '{script}';".format(script=script))
		try:
			remove(script)
		except OSError:
			error += 1

	return error
