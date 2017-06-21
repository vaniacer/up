# -*- encoding: utf-8 -*-

from django import forms
from .models import Project, Server, Update


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'desc']
		labels = {'name': 'Project name', 'desc': 'Project description'}
		widgets = {'desc': forms.Textarea(attrs={'cols': 80})}


class ServerForm(forms.ModelForm):
	class Meta:
		model = Server
		fields = ['name', 'addr', 'wdir', 'desc', 'port']
		labels = {
			'name': 'Server name', 'desc': 'Server description',
			'addr': 'SSH address', 'wdir': 'Working directory',
			'port': 'Server binding port'
		}
		widgets = {'desc': forms.Textarea(attrs={'cols': 80})}


class UpdateForm(forms.ModelForm):
	class Meta:
		model = Update
		fields = ['file', 'desc']
		labels = {'file': 'Update file', 'desc': 'Update description'}
		widgets = {
			'desc': forms.Textarea(attrs={'cols': 80}),
		}
