# -*- encoding: utf-8 -*-

from popen_call import message


def description(args, log):
	log.write('\nUpdate server {server} with update {update}\n'.format(server=args.server, update=args.update[0]))


def run(args, log):

	message('\nUnder construction\n', log)
