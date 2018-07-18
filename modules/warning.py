# -*- encoding: utf-8 -*-

from popen_call import message
from time import sleep


def warning(txt, pause, log):
	attention = [
		'   _________________________________________________    \n',
		'  / __        ___    ____  _   _ ___ _   _  ____ _  \   \n',
		' /  \ \      / / \  |  _ \| \ | |_ _| \ | |/ ___| |  \  \n',
		'/    \ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _| |   \ \n',
		'\     \ V  V / ___ \|  _ <| |\  || || |\  | |_| |_|   / \n',
		' \     \_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____(_)  /  \n',
		'  \_________________________________________________/   \n',
	]

	for line in attention:
		log.write(line)

	message('\n%s\n' % txt, log)
	message(
		""" \nIf it's not what you wished to do, you've got {pause} seconds to cancel this!
			\nFinal countdown...
		""".format(pause=pause), log
	)

	for i in range(pause):
		message('\n%s' % i, log)
		sleep(1)

	message('\n\nOk, i warned you!)\n', log)
