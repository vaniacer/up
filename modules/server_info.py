# -*- encoding: utf-8 -*-

from popen_call import my_call
from subprocess import call


def description(args, log):
	log.write("\nShow system info of server %s" % args.server)


def run(args, log):

	ssh_yes = [
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
		'''.format(server=args.server)
	]

	call(ssh_yes)

	command = [
		'ssh', args.server,
		""" printf '\n-----{{ <b>Server {server}</b> }}-----\n'
		
			printf '\n<b>Hostname:</b>\n'
			hostname
	
			printf '\n<b>Interfaces:</b>\n'
			ip a | grep 'inet ' | sed '/127.0.0.1/d; s/.*inet //g; s|/.*$||g'
	
			printf '\n<b>Memory:</b>\n'
			LANG=Us free --si -h
	
			printf '\n<b>CPU:</b>\n'
			lscpu
	
			printf '\n<b>Disk:</b>\n'
			df -h; echo; df -ih; echo; lsblk
	
			printf '\n<b>Software:</b>\n'
			uname -a; echo
			[[ -e /usr/bin/lsb_release ]] && {{ lsb_release -a; echo; }}
			[[ -e /usr/bin/java        ]] && {{ java  -version; echo; }}
			[[ -e /usr/bin/psql        ]] && {{ psql  -V      ; echo; }}
			[[ -e /usr/sbin/nginx      ]] && {{ nginx -v      ; echo; }}
	
			printf '<b>Logged in Users:</b>\n'
			who
	
			printf '<b>\nPort usage info:</b>\n'
			netstat -tulp
	
			printf '\n<b>Processes:</b>\n'
			top -bn1 | head -n30
		""".format(server=args.server)
	]

	error = my_call(command, log)
	return error
