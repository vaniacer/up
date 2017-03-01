# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group


def get_upload_to(instance, filename):
	return 'updates/%s/%s' % (instance.project.name, filename)


def get_upload_name(instance, filename):
	return filename


class Project(models.Model):
	"""Проект: web-исполнение, web-нси, web-соглашения..."""
	admn = models.ForeignKey(Group, related_name='admn', default='dummy')
	view = models.ForeignKey(Group, related_name='view', default='dummy')
	dump = models.ForeignKey(Group, related_name='dump', default='dummy')
	updt = models.ForeignKey(Group, related_name='updt', default='dummy')
	upld = models.ForeignKey(Group, related_name='upld', default='dummy')
	date = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200)
	desc = models.TextField()

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class Server(models.Model):
	"""Серверы проекта."""
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=200)
	addr = models.CharField(max_length=200)
	wdir = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	desc = models.TextField()

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class Update(models.Model):
	"""Пакеты обновлений проекта."""
	project = models.ForeignKey(Project)
	update = models.FileField(upload_to=get_upload_to)
	date = models.DateTimeField(auto_now_add=True)
	desc = models.TextField()

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.desc
