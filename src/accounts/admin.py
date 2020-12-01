from django.contrib import admin
from accounts.models import Merchant, BillingAddress, ShippingAddress

class MerchantAdmin(admin.ModelAdmin):
    model = Merchant

    list_display = [
        'name',
        'merchant_id',
        'country',
        'phone',
    ]


admin.site.register(Merchant, MerchantAdmin)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
admin.site.site_header = 'Vendora Admin'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Vendora Backend Control'