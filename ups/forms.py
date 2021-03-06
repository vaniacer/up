# -*- encoding: utf-8 -*-

from .models import Project, Server, Update, Script, Profile
from django import forms


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['script', 'update', 'cron', 'server', 'emailme', 'script_fltr', 'update_fltr', 'cron_fltr', 'server_fltr']
		labels = {
			'script':  'Show only my scripts',
			'update':  'Show only my updates',
			'server':  'Show only my servers',
			'cron':    'Show only my cron jobs',
			'emailme': 'Email me by default',
			'script_fltr': 'Default scripts filter',
			'update_fltr': 'Default updates filter',
			'server_fltr': 'Default servers filter',
			'cron_fltr':   'Default cron jobs filter',
		}


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'desc']
		labels = {'name': 'Project name', 'desc': 'Project description'}


class ServerForm(forms.ModelForm):
	class Meta:
		model = Server
		fields = ['name', 'addr', 'wdir', 'http', 'zabx', 'desc', 'port', 'slim']
		labels = {
			'name': 'Server name',
			'desc': 'Server description',
			'addr': 'SSH address',
			'wdir': 'Working directory',
			'http': 'HTTP(S) address(if available)',
			'zabx': 'Zabbix(monitoring) address(if available)',
			'port': 'Server binding port',
			'slim': 'Rsync speed limit in kb, 0 - unlimited, used in upload\\download',
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
			""" Script file.'
				SQL scripts MUST have an extension '.sql'.
				Bash scripts MUST have an extension '.sh'.
				Python scripts MUST have an extension '.py'.
				YAML playbooks MUST have an extension '.yml'.""",
			'desc': 'Script description',
		}


class ScriptCreateForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['flnm', 'desc', 'body']
		labels = {
			'flnm':
			""" File name.
				SQL scripts MUST have an extension '.sql'.
				Bash scripts MUST have an extension '.sh'.
				Python scripts MUST have an extension '.py'.
				YAML playbooks MUST have an extension '.yml'.""",
			'desc': 'Script description',
			'body': 'Script body',
		}
		widgets = {
			'body': forms.Textarea(attrs={'style': 'height: 50%; font-family: "Lucida Console", Monaco, monospace;'}),
			'flnm': forms.TextInput(attrs={'placeholder': 'File name'}),
			'desc': forms.Textarea(attrs={'style': 'height: 7%;'}),
		}


class ScriptEditForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['desc', 'body']
		labels = {'desc': 'Script description', 'body': 'Script body'}
		widgets = {
			'body': forms.Textarea(attrs={'style': 'height: 50%; font-family: "Lucida Console", Monaco, monospace;'}),
			'desc': forms.Textarea(attrs={'style': 'height: 7%;'})
		}


class HideInfoForm(forms.Form):
	tab = forms.CharField(label='', required=False)
	job_info = forms.BooleanField(label='', required=False)
	server_info = forms.BooleanField(label='', required=False)
	script_info = forms.BooleanField(label='', required=False)
	update_info = forms.BooleanField(label='', required=False)
	dbdump_info = forms.BooleanField(label='', required=False)


class PropertiesForm(forms.Form):
	properties = forms.CharField(required=True, widget=forms.Textarea(
		attrs={'style': 'height: 70%; font-family: "Lucida Console", Monaco, monospace;'}))


class StandaloneForm(forms.Form):
	standalone = forms.CharField(required=True, widget=forms.Textarea(
		attrs={'style': 'height: 70%; font-family: "Lucida Console", Monaco, monospace;'}))
