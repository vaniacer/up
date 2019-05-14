# -*- encoding: utf-8 -*-

from popen_call import my_call


def description(args, log):
	log.write('\nPrint App version on server {server}.\n'.format(server=args.server))


def run(args, log):

	error = 0
	command = [
		'ssh', args.server,
		''' cd {wdir}
			printf -- '-----{{ <b>Server {server}</b> }}-----\n'
			pass=$(grep system jboss-bas-*/standalone/configuration/krista-users.properties)
			[[ $pass ]] && pass=$(printf -- '%q' "${{pass//system=/system:}}" | base64) || exit 1
			wget -qO- http://localhost:8080/application/sysinfo/app/version --header="Authorization: Basic $pass"
		'''.format(wdir=args.wdir, server=args.server)
	]
	error += my_call(command, log)

	return error
