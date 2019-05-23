# -*- encoding: utf-8 -*-

from popen_call import my_call


def description(args, log):
	log.write("\nShow conf of server %s" % args.server)


def run(args, log):

	command = [
		'ssh', args.server,
		""" printf '\n<b>Running options</b>\n\n'
			ps axo command | grep {wdir} | grep [j]ava
			
			printf '\n<b>Jboss.properties</b>\n\n'
			cat {wdir}/jboss.properties | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'
			
			printf '\n<b>Standalone-full.xml</b>\n\n'
			cat {wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'
			for i in ${{PIPESTATUS[@]}}; {{ ((error+=$i)); }}; exit $error
		""".format(wdir=args.wdir, server=args.server)
	]

	error = my_call(command, log)
	return error
