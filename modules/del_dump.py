# -*- encoding: utf-8 -*-

from os.path import join as opj
from up.settings import DUMP_DIR
from popen_call import my_call, message


def description(args, log):
	dumps = '\n'.join(args.dump)
	log.write('\nDelete dump(s):\n{dumps}\n'.format(dumps=dumps))


def run(args, log):

	dumps = '\n'.join(args.dump)
	message('\n<b>Удаляю дамп(ы):</b>\n{dumps}\n'.format(dumps=dumps), log)

	dumps = [opj(DUMP_DIR, args.name, dump) for dump in args.dump]
	command = ['rm']
	command.extend(dumps)
	error = my_call(command, log)
	return error
