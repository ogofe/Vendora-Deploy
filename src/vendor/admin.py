from django.contrib import admin
from vendor.models import Alert


class AdminAlert(admin.ModelAdmin):
    model = Alert
    list_display = [
        'store',
        'date', 
        'priority',
    ]

admin.site.register(Alert, AdminAlert)