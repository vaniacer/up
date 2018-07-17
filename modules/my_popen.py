# -*- encoding: utf-8 -*-

from subprocess import Popen


def my_popen(command, log, pidfile):

	error = 0

	run_command = Popen(command, stdout=log, stderr=log)
	run_command.communicate()
	ppid = run_command.pid

	with open(pidfile, 'w') as f:
		f.write(str(ppid))

	cmd_error = run_command.returncode
	if cmd_error > 0:
		error = cmd_error

	run_command.wait()

	return error
