# -*- encoding: utf-8 -*-

from django.contrib.auth.models import Group


def create_dummy():
	"""Создает группу-пустышку."""
	Group.objects.get_or_create(name='dummy')


def create_groups(project):
	"""Создает группы для нового проекта, подключает созданные группы к проекту."""
	groups = ('admn', 'view', 'dump', 'updt', 'upld')
	for group in groups:
		Group.objects.get_or_create(name=project.name + '_' + group)

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

	project.save()
