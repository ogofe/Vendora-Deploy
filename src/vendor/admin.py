from django.contrib import admin
from vendor.models import Alert


class AdminAlert(admin.ModelAdmin):
    model = Alert
    list_display = [
        'store',
        'date', 
        'priority',
    ]
    actions = [
        'error'
    ]

    def error(self, request, queryset):
        e = Exception('A Failure on purpose!')
        raise e
        return e
admin.site.register(Alert, AdminAlert)