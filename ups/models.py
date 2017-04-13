# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings as conf
from django.db import models


def get_upload_to(instance, filename):
	"""Задаёт путь сохранения пакетов обновлений."""
	return conf.MEDIA_ROOT + '/updates/%s/%s' % (instance.proj.name, filename)


class Project(models.Model):
	"""Проект: web-исполнение, web-нси, web-соглашения..."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	name = models.CharField(max_length=200, unique=True)
	desc = models.TextField(max_length=255)
	slug = models.SlugField(max_length=64)

	class Meta:
		"""Добавляет доп. разрешения."""
		permissions = (
			("view_project", "Can view project"),
			("edit_project", "Can edit project"),
			("edit_server", "Can edit projects's servers"),
			("edit_update", "Can edit projects's updates"),
			("run_command", "Can run project's commands"),
			("add_server", "Can add server to project"),
			("add_update", "Can add update to project"),
			("del_server", "Can delete project's servers"),
			("del_update", "Can delete project's updates"),
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
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	name = models.CharField(max_length=200)
	addr = models.CharField(max_length=200)
	wdir = models.CharField(max_length=200)
	desc = models.TextField(max_length=255)
	proj = models.ForeignKey(Project)

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class Update(models.Model):
	"""Пакеты обновлений проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	file = models.FileField(upload_to=get_upload_to)
	desc = models.TextField(max_length=255)
	proj = models.ForeignKey(Project)

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		name = self.file.name.split('/')
		return name[2]


class History(models.Model):
	"""История проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	name = models.CharField(max_length=200)
	exit = models.CharField(max_length=200)
	cron = models.CharField(max_length=210)
	cdat = models.CharField(max_length=30)
	proj = models.ForeignKey(Project)
	user = models.ForeignKey(User)
	desc = models.TextField()

	class Meta:
		verbose_name_plural = 'events'

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name
