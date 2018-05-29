# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings as conf
from django.db import models


def update_upload_to(instance, filename):
	"""Задаёт путь сохранения пакетов обновлений."""
	return '%s/updates/%s/%s' % (conf.MEDIA_ROOT, instance.proj.name, filename)


def script_upload_to(instance, filename):
	"""Задаёт путь сохранения пакетов обновлений."""
	return '%s/scripts/%s/%s' % (conf.MEDIA_ROOT, instance.proj.name, filename)


class Project(models.Model):
	"""Проект: web-исполнение, web-нси, web-соглашения..."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	name = models.CharField(max_length=255, unique=True)
	desc = models.TextField(max_length=255)
	slug = models.SlugField(max_length=64)
	user = models.ForeignKey(User)

	class Meta:
		"""Добавляет доп. разрешения."""
		permissions = (
			("view_project", "Can view project"),
			("edit_project", "Can edit project"),
			("run_command",  "Can run commands"),
			("dld_update",   "Can download updates"),
			("dld_script",   "Can download scripts"),
			("add_server",   "Can add servers to project"),
			("add_update",   "Can add updates to project"),
			("add_script",   "Can add scripts to project"),
			("edit_server",  "Can edit projects's servers"),
			("edit_update",  "Can edit projects's updates"),
			("edit_script",  "Can edit projects's scripts"),
			("del_server",   "Can delete project's servers"),
			("del_update",   "Can delete project's updates"),
			("del_script",   "Can delete project's scripts"),
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
	opts = models.CharField(max_length=255, blank=True)  # SSH options
	addr = models.CharField(max_length=255)              # SSH address
	name = models.CharField(max_length=255)
	wdir = models.CharField(max_length=255)
	desc = models.TextField(max_length=255)
	port = models.CharField(max_length=5)
	proj = models.ForeignKey(Project)
	user = models.ForeignKey(User)

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class Update(models.Model):
	"""Пакеты обновлений проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	file = models.FileField(upload_to=update_upload_to)  # Full file path
	flnm = models.CharField(max_length=255)              # Filename only
	desc = models.TextField(max_length=255)
	proj = models.ForeignKey(Project)
	user = models.ForeignKey(User)

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.file.name.split('/')[-1]


class Script(models.Model):
	"""BASH/SQL скрипты проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	file = models.FileField(upload_to=script_upload_to)  # Full file path
	flnm = models.CharField(max_length=255)              # Filename only
	desc = models.TextField(max_length=255)
	proj = models.ForeignKey(Project)
	user = models.ForeignKey(User)
	body = models.TextField()

	def type(self):
		"""Возвращает расширение файла."""
		return self.file.name.split('.')[-1]

	def __unicode__(self):
		"""Возвращает строковое представление модели(имя файла)."""
		return self.file.name.split('/')[-1]


class Job(models.Model):
	"""Задания в кроне."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	perm = models.BooleanField(default=False)
	name = models.CharField(max_length=255)
	cron = models.CharField(max_length=255)
	cdat = models.CharField(max_length=30)
	proj = models.ForeignKey(Project)
	user = models.ForeignKey(User)
	desc = models.TextField()

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class History(models.Model):
	"""История проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	name = models.CharField(max_length=255)
	cron = models.CharField(max_length=255)
	uniq = models.CharField(max_length=255)
	cdat = models.CharField(max_length=30)
	exit = models.CharField(max_length=10)
	proj = models.ForeignKey(Project)
	user = models.ForeignKey(User)
	desc = models.TextField()

	class Meta:
		"""Название множественного числа объектов."""
		verbose_name_plural = 'events'

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name
