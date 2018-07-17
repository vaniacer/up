# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write('\nUpdate server {server} with update {update}\n'.format(server=args.server, update=args.update[0]))


def run(args, log, pid):

	message_top = ['printf', '\nUnder construction\n']
	error = my_popen(message_top, log, pid)
	return error
