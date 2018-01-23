# -*- encoding: utf-8 -*-

from .models import Project, Server, Update, Script
from django import forms
import datetime


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'desc']
		labels = {'name': 'Project name', 'desc': 'Project description'}


class ServerForm(forms.ModelForm):
	class Meta:
		model = Server
		fields = ['name', 'addr', 'wdir', 'desc', 'port']
		labels = {
			'name': 'Server name', 'desc': 'Server description',
			'addr': 'SSH address', 'wdir': 'Working directory',
			'port': 'Server binding port'
		}


class UpdateForm(forms.ModelForm):
	class Meta:
		model = Update
		fields = ['file', 'desc']
		labels = {'file': 'Update file', 'desc': 'Update description'}


class ScriptAddForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['file', 'desc']
		labels = {'file': 'Script file. SQL scripts MUST have extension \'.sql\'', 'desc': 'Script description'}


class ScriptCreateForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['flnm', 'desc', 'body']
		labels = {
			'flnm': 'File name. SQL scripts MUST have extension \'.sql\'',
			'desc': 'Script description',
			'body': 'Script body'}


class ScriptEditForm(forms.ModelForm):
	class Meta:
		model = Script
		fields = ['desc', 'body']
		labels = {'desc': 'Script description', 'body': 'Script body'}


class SerfltrForm(forms.Form):
	servers = forms.CharField(label='', required=False)


class DateTimeForm(forms.Form):
	date = datetime.datetime.now()
	datetime = forms.DateTimeField(label='', required=False, initial=date.strftime("%d.%m.%Y %H:%M"))


class HideForm(forms.Form):
	server_info = forms.BooleanField(label='', required=False)
	script_info = forms.BooleanField(label='', required=False)
	update_info = forms.BooleanField(label='', required=False)
	dbdump_info = forms.BooleanField(label='', required=False)
