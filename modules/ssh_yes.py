# -*- encoding: utf-8 -*-

from subprocess import call


def ssh_yes(server):

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
			}}
			exit
			}}
		'''.format(server=server)
	]

	call(command)
