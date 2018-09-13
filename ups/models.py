# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings as conf
from django.db import models


def update_upload_to(instance, filename):
	"""Задаёт путь сохранения пакетов обновлений."""
	return '{home}/updates/{project}/{file}'.format(
		project=instance.proj.name,
		home=conf.MEDIA_ROOT,
		file=filename,
	)


def script_upload_to(instance, filename):
	"""Задаёт путь сохранения пакетов обновлений."""
	return '{home}/scripts/{project}/{file}'.format(
		project=instance.proj.name,
		home=conf.MEDIA_ROOT,
		file=filename,
	)


class Project(models.Model):
	"""Проект: web-исполнение, web-нси, web-соглашения..."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)  # Creation date
	name = models.CharField(max_length=255, unique=True)           # Name in web interface
	desc = models.TextField(max_length=255)                        # Description
	slug = models.SlugField(max_length=64)                         # Slug
	user = models.ForeignKey(User)                                 # User relation

	class Meta:
		"""Добавляет доп. разрешения."""
		permissions = (
			("view_project", "Can view project"),

			("dld_dump",     "Can download dumps"),
			("dld_update",   "Can download updates"),
			("dld_script",   "Can download scripts"),

			("add_server",   "Can add servers to project"),
			("add_update",   "Can add updates to project"),
			("add_script",   "Can add scripts to project"),
			("add_sql",      "Can add SQL scripts to project"),
			("add_yml",      "Can add YAML scripts to project"),
			("add_sh",       "Can add BASH scripts to project"),
			("add_py",       "Can add Python scripts to project"),

			("edit_project", "Can edit project"),
			("edit_server",  "Can edit projects's servers"),
			("edit_update",  "Can edit projects's updates"),
			("edit_script",  "Can edit projects's scripts"),

			("del_server",   "Can delete project's servers"),
			("del_update",   "Can delete project's updates"),
			("del_script",   "Can delete project's scripts"),
			("del_dump",     "Can delete project's dumps"),

			("run_command",  "Can run commands"),
			("tunnel",       "Can create tunnel"),
			("run_cron",     "Can run cron commands"),
			("run_dump",     "Can run dump commands"),
			("run_update",   "Can run update commands"),
			("run_script",   "Can run project's scripts"),
			("send_dump",    "Can run command 'Send dump'"),
			("peep_pass",    "Can run command 'Peep passwords'"),
			("check_logs",   "Can view\download server's log files"),
			("check_conf",   "Can view server's standalone-full.xml"),
			("maintenance",  """Can run maintenance commands:
								Maintenance ON/OFF
								Reload config
								Restart jboss
								Start jboss
								Stop jboss
								Kill jboss
								Backup full
								Backup base
								Backup system"""),
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
	wdir = models.CharField(max_length=255, default='/var/lib/jboss')  # Work dir
	http = models.CharField(max_length=255, blank=True, null=True)     # Http\s url
	date = models.DateTimeField(auto_now_add=True, db_index=True)      # Creation date
	port = models.CharField(max_length=5, default='8080')              # Bind port, default - 8080
	addr = models.CharField(max_length=255)                            # SSH address
	name = models.CharField(max_length=255)                            # Name in web interface
	desc = models.TextField(max_length=255)                            # Description
	proj = models.ForeignKey(Project)                                  # Project relation
	user = models.ForeignKey(User)                                     # User relation

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class Update(models.Model):
	"""Пакеты обновлений проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)  # Creation date
	file = models.FileField(upload_to=update_upload_to)            # Full file path
	flnm = models.CharField(max_length=255)                        # Filename only
	desc = models.TextField(max_length=255)                        # Description
	proj = models.ForeignKey(Project)                              # Project relation
	user = models.ForeignKey(User)                                 # User relation

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.file.name.split('/')[-1]


class Script(models.Model):
	"""BASH/SQL скрипты проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)  # Creation date
	file = models.FileField(upload_to=script_upload_to)            # Full file path
	flnm = models.CharField(max_length=255)                        # Filename only
	desc = models.TextField(max_length=999)                        # Description
	proj = models.ForeignKey(Project)                              # Project relation
	user = models.ForeignKey(User)                                 # User relation
	body = models.TextField()                                      # Script body

	def type(self):
		"""Возвращает расширение файла."""
		return self.file.name.split('.')[-1]

	def __unicode__(self):
		"""Возвращает строковое представление модели(имя файла)."""
		return self.file.name.split('/')[-1]


class Job(models.Model):
	"""Задания в кроне."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)  # Creation date
	serv = models.ForeignKey(Server, blank=True, null=True)        # Server relation
	perm = models.BooleanField(default=False)                      # Permanent(run everyday) or not
	name = models.CharField(max_length=255)                        # Name in web interface
	cron = models.CharField(max_length=255)                        # Unique id
	cdat = models.CharField(max_length=30)                         # End of job time and date
	proj = models.ForeignKey(Project)                              # Project relation
	user = models.ForeignKey(User)                                 # User relation
	desc = models.TextField()                                      # Description

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name


class History(models.Model):
	"""История проекта."""
	date = models.DateTimeField(auto_now_add=True, db_index=True)  # Creation date
	serv = models.ForeignKey(Server, blank=True, null=True)        # Server relation
	name = models.CharField(max_length=255)                        # Name in web interface
	cron = models.CharField(max_length=255)                        # Unique cron id if event from cron
	uniq = models.CharField(max_length=255)                        # Unique id
	exit = models.CharField(max_length=10)                         # Command exit code
	cdat = models.CharField(max_length=30)                         # End of job time and date if event from cron
	proj = models.ForeignKey(Project)                              # Project relation
	user = models.ForeignKey(User)                                 # User relation
	desc = models.TextField()                                      # Command log

	class Meta:
		"""Название множественного числа объектов."""
		verbose_name_plural = 'events'

	def __unicode__(self):
		"""Возвращает строковое представление модели."""
		return self.name
