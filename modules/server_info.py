# -*- encoding: utf-8 -*-

from popen_call import my_call


def description(args, log):
	log.write("\nShow system info of server %s" % args.server)


def run(args, log):

	command = [
		'ssh', args.server,
		""" printf '\n<b>Date:</b>\n'
			date
			
			printf '\n<b>Hostname:</b>\n'
			hostname
	
			printf '\n<b>Interfaces:</b>\n'
			ip a
	
			printf '\n<b>Memory:</b>\n'
			LANG=Us free --si -h
	
			printf '\n<b>CPU:</b>\n'
			lscpu
	
			printf '\n<b>Disk:</b>\n'
			df -h; echo; df -ih; echo; lsblk
	
			printf '\n<b>Software:</b>\n'
			uname -a; echo
			[[ -e /etc/system-release  ]] && {{ cat /etc/system-release; echo; }}	
			[[ -e /etc/os-release      ]] && {{ cat /etc/os-release;     echo; }}	
			[[ -e /usr/bin/lsb_release ]] && {{ lsb_release -a; echo; }}
			[[ -e /usr/bin/java        ]] && {{ java  -version; echo; }}
			[[ -e /usr/bin/psql        ]] && {{ psql  -V      ; echo; }}
			[[ -e /usr/sbin/nginx      ]] && {{ nginx -v      ; echo; }}
	
			printf '<b>Logged in Users:</b>\n'
			who
	
			printf '\n<b>Port usage info:</b>\n'
			netstat -tulpn 2> /dev/null
	
			printf '\n<b>Processes:</b>\n'
			COLUMNS=120 top -bcn1 | head -n30
		""".format(server=args.server)
	]

	error = my_call(command, log)
	return error
