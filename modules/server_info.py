# -*- encoding: utf-8 -*-

from my_popen import my_popen


def description(args, log):
	log.write("\nShow system info of server %s" % args.server)


def run(args, log, pidfile):

	command = [
		'ssh', args.server,
		"""printf '\n-----{{ <b>Server {server}</b> }}-----\n'
		
		printf '\n<b>Hostname:</b>\n'
		hostname

		printf '\n<b>Interfaces:</b>\n'
		ip a | grep 'inet ' | sed '/127.0.0.1/d; s/.*inet //g; s|/.*$||g'

		printf '\n<b>Memory:</b>\n'
		LANG=Us free -h

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

		printf '<b>\nNetworking info:</b>\n'
		netstat -lnp

		printf '\n<b>Processes:</b>\n'
		top -bn1
		""".format(server=args.server)
	]

	error = my_popen(command, log, pidfile)
	return error
