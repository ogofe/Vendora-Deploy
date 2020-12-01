from django.contrib import admin
from .models import Plugin, Permission


class AdminPlugin(admin.ModelAdmin):
    model = Plugin
    list_display = [
        'name',
        'developer',
        'ours',
    ]
    search_fields = [
        'ours',
        'name',
        'developer',
    ]



admin.site.register(Permission)
admin.site.register(Plugin, AdminPlugin)