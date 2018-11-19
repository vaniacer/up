# -*- encoding: utf-8 -*-

from popen_call import my_call


def description(args, log):
	log.write("\nTest ssh connection to server %s" % args.server)


def run(args, log):

	command = [
		'expect', '-c',
		''' spawn ssh {server}
			expect {{
				"(yes/no)?" {{
					send "yes\n"
					expect {{
						"assword:" {{ exit }}
						"$ "       {{ send "exit\n" }}
					}}
				}}
				"assword:" {{ exit }}
				"$ "       {{ send "exit\n" }}
				"fail"     {{ exit 1 }}
				timeout    {{ exit 1 }}
			}}
		'''.format(server=args.server)
	]

	error = my_call(command, log)
	return error
