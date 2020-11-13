from django.db import models
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


GENDER = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))

class Manager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('An email address is required')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, max_length=200, verbose_name='Email Address')
    gender = models.CharField(max_length=1, choices=GENDER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = Manager()
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Attrs:
        has_store = False
        
    def name(self):
        return f'{self.first_name} {self.last_name}'

class BillingAddress(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
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
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=35)
    city = models.CharField(max_length=30)
    address = models.TextField()
    opt_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.name()
    
    class Meta:
        verbose_name_plural = 'Shipping Addresses'