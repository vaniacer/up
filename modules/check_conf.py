# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write("\nShow conf of server %s" % args.server)


def run(args, log, pidfile):

	command = [
		'ssh', args.server,
		"""printf '\n-----{{ <b>Server {server}</b> }}-----\n'
		
		printf '\n<b>Java options</b>\n\n'
		ps axo command | grep {wdir} | grep [j]ava

		printf '\n<b>Standalone-full.xml</b>\n\n'
		cat {wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'
		""".format(wdir=args.wdir, server=args.server)
	]

	error = my_popen(command, log, pidfile)
	return error
