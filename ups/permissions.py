# -*- encoding: utf-8 -*-

from django.http import Http404


def check_perm(perm, obj, user):
	"""Проверяет разрешения объекта."""
	if not user.has_perm(perm, obj):
		raise Http404
