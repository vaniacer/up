# -*- encoding: utf-8 -*-

from popen_call import my_call


def description(args, log):
	log.write("\nShow system info of server %s" % args.server)


def run(args, log):

	command = [
		'ssh', args.server,
		""" printf '\n-----{{ <b>Server {server}</b> }}-----\n'
		
			printf '<b>\nИщу jboss процес </b>\n'
			ps axu | head -n1
			ps axu | grep {wdir} | grep [j]ava \
				&& {{ printf '\nПриложение работает\n'; }} \
				|| {{ printf '\nПриложение не работает\n'; ((error++)); }}

			printf '<b>\nПроверяю доступность порта {port}</b>\n'
			netstat -tulpn 2> /dev/null | grep ':{port} ' \
				&& {{ printf '\nПорт открыт\n'; }} \
				|| {{ printf '\nПорт закрыт\n'; ((error+=2)); }}

			printf '<b>\nПроверяю http доступ(локально)</b>\n'
			wget -qO- -T10 -t1 'http://localhost:{port}/application' > /dev/null \
				&& {{ printf '\nДоступ есть\n'; }} \
				|| {{ printf '\nДоступа нет\n'; ((error+=3)); }}
				
			exit $error
		""".format(server=args.server, port=args.port, wdir=args.wdir)
	]

	error = my_call(command, log)
	return error
