# -*- encoding: utf-8 -*-

from django.contrib import admin
from models import Project, Server, Update

admin.site.register(Project)
admin.site.register(Server)
admin.site.register(Update)