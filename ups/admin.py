# -*- encoding: utf-8 -*-

from models import Project, Server, Update, Script, History, Job
from guardian.admin import GuardedModelAdmin
from django.contrib import admin


class ProjectAdmin(GuardedModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ('name', 'slug', 'date')
	search_fields = ('name', 'content')
	ordering = ('-date',)
	date_hierarchy = 'date'


admin.site.register(Project, ProjectAdmin)
admin.site.register(History)
admin.site.register(Server)
admin.site.register(Update)
admin.site.register(Script)
admin.site.register(Job)
