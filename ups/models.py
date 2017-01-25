# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group


class Project(models.Model):
	"""Проект: web-исполнение, web-нси, web-соглашения"""
	name = models.CharField(max_length=200)
	desc = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	view = models.ForeignKey(Group, related_name='view')
	dump = models.ForeignKey(Group, related_name='dump')
	updt = models.ForeignKey(Group, related_name='updt')
	upld = models.ForeignKey(Group, related_name='upld')

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class Server(models.Model):
	"""Серверы проекта."""
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=200)
	addr = models.CharField(max_length=200)
	wdir = models.CharField(max_length=200)
	desc = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name