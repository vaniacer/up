# -*- encoding: utf-8 -*-

from os import urandom
from base64 import b64encode


def uniq():
	"""Создает случайную последовательность символов."""
	return str(b64encode(urandom(6), 'dfsDFAsfsf'))
