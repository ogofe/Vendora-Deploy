from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import MinLengthValidator


User = settings.AUTH_USER_MODEL
SOCIAL_MEDIA = (
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter'),
    ('instagram', 'Instagram'),
    ('craigslist', 'Craigslist'),
)

PAYMENT_CARRIERS = (
    ('remita', 'https://remita.net/'),
    ('paypal', 'http://paypal.com/'),
    ('stripe', 'http://stripe.com/'),
    ('mastercard', 'http://developers.mastercard.com/'),
)

class Store(models.Model):
    name = models.CharField(max_length=30, unique=True)
    logo = models.FileField(upload_to='stores/logos', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    currency = models.ForeignKey('Currency', default=1, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField('Product', blank=True, related_name='products')
    alerts = models.ManyToManyField('vendor.Alert', blank=True, related_name='alerts')
    carousels = models.ManyToManyField('Carousel', blank=True, related_name='carousels')
    customers = models.ManyToManyField(User, blank=True, related_name='customers')
    platforms = models.ManyToManyField('Social', blank=True, related_name='platforms')
    payment_methods = models.ManyToManyField('PaymentMethod', blank=True, related_name='payment_methods')
    invoices = models.ManyToManyField('Invoice', blank=True)
    campaigns = models.ManyToManyField('Campaign', blank=True, related_name='campaigns')
    coupons = models.ManyToManyField('Coupon', blank=True, related_name='coupon')
    is_open = models.BooleanField(default=True)
    date_opened = models.DateField(auto_now=True)
    blocked = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('store:store-view', kwargs={"store_name": self.name})

    def max(self):
        if self.products.all().count() > 0:
            price = self.products.all().order_by('-price')
            return str(price[0].price)
        return 0 

        
    def min(self):
        if self.products.all().count() > 0:
            price = self.products.all().order_by('price')
            return str(price[0].price)
        return 0

    def max_int(self):
        if self.products.all().count() > 0:
            price = self.products.all().order_by('-price')
            return price[0].price
        return 0
    

    def min_int(self):
        if self.products.all().count() > 0:
            price = self.products.all().order_by('price')
            return price[0].price
        return 0
    
    def get_available_categories(self):
        cats = []
        for item in self.products.all():
            if not item.category in cats or item.category in cats:
                for cat in item.sub_cats.all():
                    if not cat in cats:
                        cats.append(cat)
        return cats
    
    def get_cats(self):
        cats = []
        for item in self.products.all():
            if not item.category in cats or item.category in cats:
                for cat in item.sub_cats.all():
                    if not cat in cats:
                        cats.append(cat)
        return cats[:3]

    class Attrs:
        template = 'default'
        font = 'default',
        font_size = 'default'
        background = 'default'
        newly_created = True
        is_admin_logged_in = True
        integrations = []
        bank_name = ''  # e.g first bank, paypal
        acc_name = ''   # e.g Joel Tanko
        acc_nummber = '' # e.g 3112330982, example@paypal.com
        access = ''
        refresh = ''
        api_public =  ''
        api_private = ''

    class Header:
        background = 'default'
        font = 'default',
        font_size = 'default'
        title = ''
        sub_title = ''
        content = ''
        hidden = False

    def __str__(self):
        return self.name
    
    def worth(self):
        items = self.products.all()
        worth = 0
        for item in items:
            worth += item.price * item.quantity
        return worth
    
    def has_products(self):
        if self.products.all().count() > 0:
            return True
        return False


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    worth = models.DecimalField(decimal_places=2, max_digits=10)
    validity = models.DateField(blank=True, null=True)
    been_used_by = models.ManyToManyField(User, blank=True, related_name='users')

    def __str__(self):
        return self.code

    def redeem(self, invoice):
        users = self.been_used_by.all()
        for user in users:
            if not user in users:
                invoice.amount -= self.worth
                invoice.save()
                users.add(user)
                return True
            return True

            

class Social(models.Model):
    link = models.CharField(max_length=200, unique=True)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=SOCIAL_MEDIA)

    def __str__(self):
        return self.type.title()
    

class Carousel(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    header = models.CharField(max_length=300)
    items = models.ManyToManyField('CarouselItem', blank=True, related_name='items')
    hidden = models.BooleanField(default=False)
    class Attrs:
        background = 'default'
        font = 'default'
        font_size = 'default'

class CarouselItem(models.Model):
    carousel = models.ForeignKey('Carousel', on_delete=models.CASCADE, related_name='carousel')
    caption = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='stores/carousel/', blank=True, null=True)

class Campaign(models.Model):
    title = models.CharField(max_length=30)
    platforms = models.ManyToManyField('Social', blank=True)
    items = models.ManyToManyField('CampaignItem', blank=True, related_name='items')

class CampaignItem(models.Model):
    item = models.ForeignKey('Product', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='campaign')

class Currency(models.Model):
    code = models.CharField(max_length=5)
    symbol = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.code
    

class PaymentMethod(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=PAYMENT_CARRIERS)
    gateway_link = models.CharField(max_length=200, blank=True, unique=True)   # link to payment api gateway. e.g https://remita.net/api/payment
    user_id = models.CharField(max_length=30, blank=True, null=True)    # user_id from api (if given)
    secret_key = models.CharField(max_length=300, blank=True)   # Gateway API secret key
    public_key = models.CharField(max_length=300, blank=True) # Public Key

    def setup(self):
        "Setup this payment method for this store"
        self.store.payment_methods.add(self)
        return True
    
    def __str__(self):
        return self.type
    

class Invoice(models.Model):
    issuer = models.ForeignKey('Store', on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    number = models.CharField(unique=True, validators=[MinLengthValidator(11),], max_length=11)
    status = models.CharField(max_length=7, choices=(('paid', 'Paid'), ('pending', 'Pending'), ('not_paid', 'Not Paid')),
    default='pending')
    date_created = models.DateTimeField(auto_now=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)

    def _number(self):
        return str(self.number)

    
class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem', blank=True, related_name='items')
    

    def __str__(self):
        return str(self.owner)

    def count(self):
        return self.items.all().count()
    
    def total(self):
        amt = 0
        for item in self.items.all():
            if not item.item.discount_price:
                amt += item.item.price * item.quantity
            if item.item.discount_price:
                amt += int(item.item.discount_price) * item.quantity
        return amt
    
    def clear(self):
        for item in self.items.all():
            item.delete()
        return self
            
    

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    item = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=3, blank=True, null=True)
    color = models.CharField(max_length=3, blank=True, null=True)

    
    def __str__(self):
        return str(self.item.name)
    

    def add_to_cart(self, cart):
        cart.items.add(self)
        return cart
    
    def total(self):
        if not self.item.discount_price:
            amt = self.quantity * self.item.price
            return amt
        amt = self.quantity * self.item.price
        return amt

class WishList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    items = models.ManyToManyField('WishItem', blank=True)

    def __str__(self):
        return self.owner
    
    def count(self):
        return self.items.all().count()
    

class WishItem(models.Model):
    list = models.ForeignKey('WishList', on_delete=models.CASCADE)
    item = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Product(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='stores/products')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True)
    sizes = models.ManyToManyField('SizeVariant', blank=True)
    colors = models.ManyToManyField('ColorVariant', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')
    sub_cats = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.name
    
    def currency(self):
        currency = self.store.currency
        return currency.code + f' : {currency.symbol}'

    def add_to_cart(self, cart, cart_item):
        cart.items.add(cart_item)
        cart.save()

    def discount(self):
        if self.discount_price:
            discount = round(((self.price - self.discount_price) * 100) / self.price, 2)
            return f'{discount}%'
        return '0%'
        


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class ColorVariant(models.Model):
    item = models.ForeignKey('Product', on_delete=models.CASCADE)
    option = models.CharField(max_length=20)
    image = models.FileField(upload_to='stores/product/variants/', blank=True)

    def __str__(self):
        return self.item
    

class SizeVariant(models.Model):
    option = models.CharField(max_length=4)

    def __str__(self):
        return self.option
    

