# -*- encoding: utf-8 -*-

from django.contrib.auth.models import Group


def create_dummy():
	"""Создает группу-пустышку."""
	Group.objects.get_or_create(name='dummy')


def create_groups(project_name):
	"""Создает группы для каждого нового проекта."""
	groups = ('admn', 'view', 'dump', 'updt', 'upld')
	for group in groups:
		Group.objects.get_or_create(name=project_name + '_' + group)


def check_groups(project):
	"""Подключает созданные группы к проекту."""
	if project.admn.name == 'dummy':
		for group in Group.objects.all():
			if group.name == project.name + '_admn':
				project.admn = group
			elif group.name == project.name + '_view':
				project.view = group
			elif group.name == project.name + '_dump':
				project.dump = group
			elif group.name == project.name + '_updt':
				project.updt = group
			elif group.name == project.name + '_upld':
				project.upld = group
