# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group


def get_upload_to(instance, filename):
	"""Задаёт путь сохранения пакетов обновлений."""
	return 'updates/%s/%s' % (instance.project.name, filename)


class Project(models.Model):
	"""Проект: web-исполнение, web-нси, web-соглашения..."""
	admn = models.ForeignKey(Group, related_name='admn', default='dummy')
	view = models.ForeignKey(Group, related_name='view', default='dummy')
	dump = models.ForeignKey(Group, related_name='dump', default='dummy')
	updt = models.ForeignKey(Group, related_name='updt', default='dummy')
	upld = models.ForeignKey(Group, related_name='upld', default='dummy')
	name = models.CharField(max_length=200, unique=True)
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	desc = models.TextField()
	slug = models.SlugField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		"""Добавляет доп. разрешения."""
		permissions = (
			("view_project", "Can view project"),
		)
		get_latest_by = 'date'

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return {'project_slug': self.slug}


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

	class Meta:
		"""Добавляет разрешение на просмотр."""
		permissions = (
			("view_server", "Can view server"),
		)


class Update(models.Model):
	"""Пакеты обновлений проекта."""
	project = models.ForeignKey(Project)
	update = models.FileField(upload_to=get_upload_to)
	date = models.DateTimeField(auto_now_add=True)
	desc = models.TextField()

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		name = self.update.name.split('/')
		return name[2]

	class Meta:
		"""Добавляет разрешение на просмотр."""
		permissions = (
			("view_update", "Can view update"),
		)
