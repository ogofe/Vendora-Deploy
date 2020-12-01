from django.db import models
from django.contrib.auth.models import User



Model = models.Model
class Merchant(Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    merchant_id = models.CharField(max_length=50, blank=True)
    avatar = models.FileField(upload_to='profile/', blank=True, null=True)
    stores = models.ManyToManyField('store.Store', blank=True)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    tokens = models.ManyToManyField('Token', blank=True, related_name='tokens')
    bank_name = models.CharField(max_length=150)
    bank_acct_name = models.CharField(max_length=150)
    bank_acct_num = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name()

    def name(self):
        return f'{self.profile.first_name} {self.profile.last_name}'


class Token(Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    api = models.URLField()
    name = models.CharField(max_length=50)
    token = models.CharField(max_length=200)

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=35)
    city = models.CharField(max_length=30)
    address = models.TextField()
    opt_address = models.TextField(blank=True, null=True)
    card_number = models.CharField(max_length=24)
    card_name = models.CharField(max_length=24)
    card_cvv = models.CharField(max_length=24)
    card_exp = models.DateField()

    def __str__(self):
        return self.user.name()
    
    class Meta:
        verbose_name_plural = 'Billing Addresses'

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=35)
    city = models.CharField(max_length=30)
    address = models.TextField()
    opt_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.name()
    
    class Meta:
        verbose_name_plural = 'Shipping Addresses'