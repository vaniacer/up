# -*- encoding: utf-8 -*-

from django.contrib import admin
from models import Project, Server, Update, History
from guardian.admin import GuardedModelAdmin


class ProjectAdmin(GuardedModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ('name', 'slug', 'date')
	search_fields = ('name', 'content')
	ordering = ('-date',)
	date_hierarchy = 'date'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Server)
admin.site.register(Update)
admin.site.register(History)
