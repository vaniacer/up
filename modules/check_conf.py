# -*- encoding: utf-8 -*-


def description(server):
	return "\nShow conf of server:\n%s" % server


def run(server, port, wdir):

	command = [
		"""
		printf '\n<b>Java options</b>\n\n'
		ps axo command | grep {wdir} | grep [j]ava

		printf '\n<b>Standalone-full.xml</b>\n\n'
		cat {wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'
		""".format(wdir=wdir)
	]

	message = '\n-----{ <b>Server %s</b> }-----\n' % server

	return command, message

