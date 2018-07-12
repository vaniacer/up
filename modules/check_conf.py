# -*- encoding: utf-8 -*-


def description(args):
	return "\nShow conf of server:\n%s" % args.server


def run(args):

	command = [
		'ssh', args.server,
		"""
		printf '\n<b>Java options</b>\n\n'
		ps axo command | grep {wdir} | grep [j]ava

		printf '\n<b>Standalone-full.xml</b>\n\n'
		cat {wdir}/jboss-bas-*/standalone/configuration/standalone-full.xml | sed 's|<|\&lt\;|g;s|>|\&gt\;|g'
		""".format(wdir=args.wdir)
	]

	message = {'top': '\n-----{ <b>Server %s</b> }-----\n' % args.server, 'bot': ''}
	dick = {'command': command, 'message': message, 'download': ''}

	return dick
