import os
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import MinLengthValidator
from django.dispatch import Signal
from accounts.models import Merchant
from django.contrib.auth.models import User
from django.core.files import File


SOCIAL_MEDIA = (
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter'),
    ('instagram', 'Instagram'),
    ('craigslist', 'Craigslist'),
    ('tumblr', 'Tumblr'),
    ('craigslist', 'Craigslist'),
)

PAYMENT_CARRIERS = (
    ('remita', 'https://remita.net/'),
    ('vougepay', 'https://vougepay.com/api'),
    ('paypal', 'http://paypal.com/'),
    ('stripe', 'http://stripe.com/'),
    ('mastercard', 'http://developers.mastercard.com/'),
)

TEMPLATES_DIR = os.path.join(settings.BASE_DIR, 'templates/store/')
default_templates_dir = TEMPLATES_DIR
# default_templates_dir = os.path.join(TEMPLATES_DIR, 'default')

def create_random_id(last:int=None) -> int :
    _id = '717'
    if last:
        if last < 10:
            _id = str(last) + _id
            
        


class Store(models.Model):
    name            = models.CharField(max_length=30, unique=True)
    owner           = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='owner')
    logo            = models.FileField(upload_to='stores/logos', blank=True)
    currency        = models.ForeignKey('Currency', default=1, on_delete=models.DO_NOTHING)
    date_opened     = models.DateField(auto_now=True)
    staff_limit     = models.IntegerField(default=2)
    products        = models.ManyToManyField('Product', blank=True, related_name='products')
    customers       = models.ManyToManyField(User, blank=True, related_name='customers')
    carousel        = models.ManyToManyField('CarouselItem', blank=True, related_name='carousel')
    platforms       = models.ManyToManyField('Social', blank=True, related_name='platforms')
    payment_methods = models.ManyToManyField('PaymentMethod', blank=True, related_name='payment_methods')
    campaigns       = models.ManyToManyField('Campaign', blank=True, related_name='campaigns')
    coupons         = models.ManyToManyField('Coupon', blank=True, related_name='coupon')
    plugins         = models.ManyToManyField("plugins.Plugin", blank=True)
    staff_accounts  = models.ManyToManyField(User, default=owner)
    custom_css      = models.FileField(upload_to='stores/css', blank=True)
    custom_js       = models.FileField(upload_to='stores/js', blank=True)
    template_dir    = models.FilePathField(allow_folders=True, allow_files=False, blank=True,
                                           max_length=400, path=default_templates_dir,
                                           default=default_templates_dir)
    is_open         = models.BooleanField(default=True)
    blocked         = models.BooleanField(default=False)
    is_setup        = models.BooleanField(default=False)
    slug            = models.SlugField(blank=True)
    
    class Attrs:
        newly_created = True
        is_admin_logged_in = True
        integrations = []
        access = ''
        refresh = ''
        api_public =  ''
        api_private = ''

    def get_absolute_url(self):
        return reverse("store:store-view", kwargs={"slug": self.slug})
    
        
    def _products(self):
        return self.products.all()

    def setup(self):
        self.install_default_plugins()      
        self.slug = self.slugify()  
        # if the store was accidentaly marked for setup
        # don't  overwrite it's files
        path = str(settings.MEDIA_ROOT)
        if not self.is_setup: 
            csspath = str(os.path.join(settings.MEDIA_ROOT, 'stores/css/'))
            jspath = str(os.path.join(settings.MEDIA_ROOT, 'stores/js/'))
            try:
                os.chdir(os.path.join(settings.MEDIA_ROOT, 'stores/'))
                os.mkdir('css')
                os.mkdir('js')
            except:
                pass
            
            # generate file name from path and storename
            css_filename = csspath + self.namify() + '-custom-css.css'
            js_filename = jspath + self.namify() + '-custom-js.js'
            
            # Creating css file object
            with open(css_filename, 'w') as cssfile:
                _file = File(cssfile)
                _file.write('/* Edit your store using this css file */\n')
                _file.close()
                self.custom_css.name = _file.name.replace(path, '')
            # js file object
            with open(js_filename, 'w') as jsfile:
                _file = File(jsfile)
                _file.write('/* Add Custom actions to %s using this javascript file */\n' % self.name)
                _file.close()
                self.custom_js.name = _file.name.replace(path, '')
            # save the changes
            self.is_setup = True
            self.template_dir = 'default'
            self.save()
        return True
    

    def slugify(self):
        "fill the slug field with a generated slug"
        slug = self.name.lower().replace(' ', '_').replace("'", '-')
        return slug

    def install_default_plugins(self):
        "Installs the default plugins to a store"
        from plugins.models import Plugin
        plugins = list(Plugin.objects.filter(ours=True))
        for plugin in plugins:
            self.plugins.add(plugin)
        self.save()
        return True

    def is_staff(self, user):
        "returns True if user is a staff in this store"
        if user in self.staff_accounts.all():
            return True
        return False

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

        
    def namify(self)-> str:
        "Converts white spaces to underscores"
        name = self.name.replace(' ', '_')
        return name


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
    
class CarouselItem(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='store')
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
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    api = models.CharField(max_length=30, choices=PAYMENT_CARRIERS)
    token = models.CharField(max_length=30, blank=True, null=True)    # user_id from api (if given)

    def setup(self):
        "Setup this payment method for this store"
        self.store.payment_methods.add(self)
        return True
    
    def __str__(self):
        return self.api
    


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
        return f'{self.owner}\'s Wish list'
    
    def count(self):
        return self.items.all().count()
    
    
    def clear(self):
        for i in self.items.all():
            i.delete()

class WishItem(models.Model):
    list = models.ForeignKey('WishList', on_delete=models.CASCADE)
    item = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.list.owner}\'s wishlist item | Store : {self.list.store} '
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='stores/products')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    sizes = models.ManyToManyField('SizeVariant', blank=True)
    colors = models.ManyToManyField('ColorVariant', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')
    sub_cats = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def _store(self):
        return self.store

    def __str__(self):
        return self.name
    
    def tag(self):
        tag = ''
        try:
            tag = list(self.tags.all())[0]
        except: # no tags on item
            tag = None
        return tag
    
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
    
    

DELIVERY_STATUS = (
    ('null', 'Not-Started'),
    ('moving', 'On Route'),
)

class Order(models.Model):
    store = models.OneToOneField(Store, models.CASCADE)
    invoice = models.OneToOneField(Invoice, models.CASCADE)
    tracking_id = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=100, choices=DELIVERY_STATUS, default='null')
    
    def __str__(self):
        return 'Order for Shopper: %s | Store : %s' % (self.person(), self.store)
    
    def person(self):
        "return the shopper's username"
        return self.invoice.payer
    
    def items(self):
        return list(self.invoice.cart.items.all())