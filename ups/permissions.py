# -*- encoding: utf-8 -*-

from django.http import Http404


def check_perm_or404(perm, obj, user):
	"""Проверяет разрешение на доступ урл объекта."""
	if not user.has_perm(perm, obj):
		raise Http404


def check_permission(perm, obj, user):
	"""Проверяет разрешения объекта."""
	if user.has_perm(perm, obj):
		return True
	else:
		return False
