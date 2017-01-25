# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group


# Create dummy group
dummy = Group.objects.get_or_create(name='dummy')

class Project(models.Model):
	"""Проект: web-исполнение, web-нси, web-соглашения"""
	name = models.CharField(max_length=200)
	desc = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	view = models.ForeignKey(Group, related_name='view', default='dummy')
	dump = models.ForeignKey(Group, related_name='dump', default='dummy')
	updt = models.ForeignKey(Group, related_name='updt', default='dummy')
	upld = models.ForeignKey(Group, related_name='upld', default='dummy')

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