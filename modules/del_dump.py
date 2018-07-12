# -*- encoding: utf-8 -*-

import os
from up.settings import DUMP_DIR


def description(args):
	dumps = '\n'.join(args.dump)
	return "\nDelete dump(s):\n{dumps}\n".format(dumps=dumps)


def run(args):

	dumps = '\n'.join(args.dump)
	message = {'top': '\n<b>Удаляю дамп(ы):</b>\n{dumps}\n'.format(dumps=dumps), 'bot': ''}

	dumps = [os.path.join(DUMP_DIR, args.proname, dump) for dump in args.dump]
	command = ['rm']
	command.extend(dumps)
	dick = {'command': command, 'message': message, 'download': ''}

	return dick
