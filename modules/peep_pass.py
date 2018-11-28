# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nPeep passwords from file krista-users.properties of server %s\n' % args.server)


def run(args, log):

	message('\n-----{{ <b>Server {server}</b> }}-----\n\n<b>Подглядываю пароли, никому не показывай;)</b>\n'.format(
		wdir=args.wdir, server=args.server), log)
	command = ['ssh', args.server, 'cat {home}/jboss-bas-*/standalone/configuration/krista-users.properties'.format(
		home=args.wdir
	)]
	error = my_call(command, log)
	return error
