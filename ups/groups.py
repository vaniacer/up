# -*- encoding: utf-8 -*-

from django.contrib.auth.models import Group


def create_dummy():
	"""Создает группу-пустышку, необходимую(пока?) при создании нового проекта."""
	Group.objects.get_or_create(name='dummy')


def delete_groups(project):
	"""Удаляет группы проекта."""
	project.admn.delete()
	project.view.delete()
	project.dump.delete()
	project.updt.delete()
	project.upld.delete()


def create_groups(project, user):
	"""Создает группы для нового проекта, подключает созданные группы к проекту."""
	groups = ('admn', 'view', 'dump', 'updt', 'upld')

	for group in groups:

		new_group = Group.objects.get_or_create(name=project.name + '_' + group)  # returns tuple
		user.groups.add(new_group[0])
		# print new_group

		if new_group[0].name == project.name + '_admn':
			project.admn = new_group[0]
		elif new_group[0].name == project.name + '_view':
			project.view = new_group[0]
		elif new_group[0].name == project.name + '_dump':
			project.dump = new_group[0]
		elif new_group[0].name == project.name + '_updt':
			project.updt = new_group[0]
		elif new_group[0].name == project.name + '_upld':
			project.upld = new_group[0]

	project.save()
