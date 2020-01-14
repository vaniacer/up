# -*- encoding: utf-8 -*-

from popen_call import my_call, message


def description(args, log):
	log.write('\nStart jboss on server %s\n' % args.server)


def run(args, log):

	message('\n<b>Выполняю jboss.start</b>\n'.format(wdir=args.wdir), log)
	command = ['ssh', args.server, '{wdir}/krupd jboss.start'.format(wdir=args.wdir)]
	error = my_call(command, log)
	if error:
		command = [
			'ssh', args.server,
			'''	cd {wdir}/jboss-bas-*/standalone/deployments
				for file in *.failed; {{
					echo "------------{{ $file }}------------"
					cat $file			
				}}
			'''.format(wdir=args.wdir)]
		error += my_call(command, log)
	return error
