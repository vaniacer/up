# -*- encoding: utf-8 -*-

from subprocess import Popen, call


def message(txt, log):
	log.write(txt)
	log.flush()


def my_call(command, log):

	error = call(command, stdout=log, stderr=log)
	return error


def my_popen(command, log, pidfile):

	run_command = Popen(command, stdout=log, stderr=log)
	run_command.communicate()
	pid = run_command.pid

	with open(pidfile, 'w') as f:
		f.write(str(pid))

	error = run_command.returncode
	run_command.wait()

	return error
