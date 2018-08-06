# -*- encoding: utf-8 -*-

from sys import argv
from subprocess import call, check_output

keys = argv[1::]
command = ['kill']
pids_raw = check_output(['ps', 'a', '-o', 'pid,cmd'])
pid_list = pids_raw.split('\n')
for key in keys:
	command.extend([s.lstrip().split(' ')[0] for s in pid_list if key in s])

call(command)
