from django.contrib import admin
from store.models import (
    Store, Product,
    Category, Tag,
    Carousel, CarouselItem,
    Campaign, CampaignItem,
    Cart, CartItem,
    ColorVariant, SizeVariant,
    PaymentMethod,
    Coupon, Social,
    WishList, WishItem,
    Invoice, Currency, 
)

class AdminStore(admin.ModelAdmin):
    model = Store
    search_fields = ('name', 'products', 'owner')
    list_display = [
        'name',
        'owner',
        'currency',
        'worth',
    ]

class AdminProduct(admin.ModelAdmin):
    model = Product
    search_fields = ('name', 'store', 'tags')
    list_display = [
        'store',
        'name',
        'price',
        'currency',
        'quantity',
    ]

class AdminInvoice(admin.ModelAdmin):
    model = Invoice
    list_display = [
        '_number',
        'issuer',
        'status',
        'payer',
        'amount',
        'date_created',
    ]

admin.site.register(Store, AdminStore)
admin.site.register(Product, AdminProduct)
admin.site.register(Currency)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Social)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(SizeVariant)
admin.site.register(ColorVariant)
admin.site.register(Coupon)
admin.site.register(Invoice, AdminInvoice)
# admin.site.register(I)
# admin.site.register(Store)