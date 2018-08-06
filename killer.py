# -*- encoding: utf-8 -*-

from sys import argv
from subprocess import call, check_output

command = ['kill']
id_list = argv[1::]
pids_raw = check_output(['ps', 'a', '-o', 'pid,cmd'])
pid_list = pids_raw.split('\n')
for pid_id in id_list:
	command.extend([s.lstrip().split(' ')[0] for s in pid_list if pid_id in s])

call(command)
