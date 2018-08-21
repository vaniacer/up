# -*- encoding: utf-8 -*-

from .models import Project, Server, Update, Script
from django import forms


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'desc']
		labels = {'name': 'Project name', 'desc': 'Project description'}


class ServerForm(forms.ModelForm):
	class Meta:
		model = Server
		fields = ['name', 'addr', 'wdir', 'http', 'desc', 'port']
		labels = {
			'name': 'Server name', 'desc': 'Server description',
			'addr': 'SSH address', 'wdir': 'Working directory',
			'http': 'HTTP(S) address(if available)',
			'port': 'Server binding port'
		}


class UpdateForm(forms.ModelForm):
	class Meta:
		model = Update
		fields = ['file', 'desc']
		labels = {'file': 'Update file', 'desc': 'Update description'}


class DumpForm(forms.Form):
	file = forms.FileField(label='PG dumpg in .gz format')


class ScriptAddForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['file', 'desc']
		labels = {
			'file':
			'Script file.'
			' SQL scripts MUST have an extension \'.sql\'.'
			' YAML playbooks MUST have an extension \'.yml\'.'
			' Bash scripts MUST have an extension \'.sh\'.'
			' Python scripts MUST have an extension \'.py\'.',
			'desc': 'Script description',
		}


class ScriptCreateForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['flnm', 'desc', 'body']
		labels = {
			'flnm':
			'File name.'
			' SQL scripts MUST have an extension \'.sql\'.'
			' YAML playbooks MUST have an extension \'.yml\'.'
			' Bash scripts MUST have an extension \'.sh\'.'
			' Python scripts MUST have an extension \'.py\'.',
			'desc': 'Script description',
			'body': 'Script body',
		}
		widgets = {
			'body': forms.Textarea(attrs={'style': 'height: 50%;font-family: "Lucida Console", Monaco, monospace;'}),
			'desc': forms.Textarea(attrs={'style': 'height: 7%;'})
		}


class ScriptEditForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['desc', 'body']
		labels = {'desc': 'Script description', 'body': 'Script body'}
		widgets = {
			'body': forms.Textarea(attrs={'style': 'height: 50%;font-family: "Lucida Console", Monaco, monospace;'}),
			'desc': forms.Textarea(attrs={'style': 'height: 7%;'})
		}


class HideInfoForm(forms.Form):
	tab = forms.CharField(label='', required=False)
	job_info = forms.BooleanField(label='', required=False)
	server_info = forms.BooleanField(label='', required=False)
	script_info = forms.BooleanField(label='', required=False)
	update_info = forms.BooleanField(label='', required=False)
	dbdump_info = forms.BooleanField(label='', required=False)


class ServersFilterForm(forms.Form):
	servers = forms.CharField(label='', required=False)


class ScriptsFilterForm(forms.Form):
	scripts = forms.CharField(label='', required=False)


class UpdatesFilterForm(forms.Form):
	updates = forms.CharField(label='', required=False)


class DumpsFilterForm(forms.Form):
	dumps = forms.CharField(label='', required=False)


class JobsFilterForm(forms.Form):
	jobs = forms.CharField(label='', required=False)
