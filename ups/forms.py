# -*- encoding: utf-8 -*-

from django  import forms
from .models import Project, Server


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'desc', 'admn', 'view', 'dump', 'updt', 'upld']
		labels = {'name': 'Project name',
				  'desc': 'Project description',
				  'admn': 'Admin group',
				  'view': 'View group',
				  'dump': 'DB access group',
				  'updt': 'Update group',
				  'upld': 'Upload group'}


class ServerForm(forms.ModelForm):
	class Meta:
		model = Server
		fields = ['name', 'addr', 'wdir', 'desc']
		labels = {'name': 'Server name', 'desc': 'Server description', 'addr': 'IP addres', 'wdir': 'Working directory'}
		widgets = {'desc': forms.Textarea(attrs={'cols': 80})}