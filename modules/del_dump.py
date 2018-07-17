# -*- encoding: utf-8 -*-

import os
from my_popen import my_popen
from up.settings import DUMP_DIR


def description(args, log):
	dumps = '\n'.join(args.dump)
	log.write('\nDelete dump(s):\n{dumps}\n'.format(dumps=dumps))


def run(args, log, pid):

	dumps = '\n'.join(args.dump)
	message_top = ['printf', '\n<b>Удаляю дамп(ы):</b>\n{dumps}\n'.format(dumps=dumps)]
	my_popen(message_top, log, pid)

	dumps = [os.path.join(DUMP_DIR, args.proname, dump) for dump in args.dump]
	command = ['rm']
	command.extend(dumps)
	error = my_popen(command, log, pid)
	return error
