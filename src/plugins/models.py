from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from store.models import Store

class Plugin(models.Model):
    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=50)
    developer = models.EmailField()
    permissions = models.ManyToManyField("Permission", related_name='permissions')
    approved = models.BooleanField(default=False)
    ours = models.BooleanField(default=False)
    details = models.TextField()
    src_destination = models.URLField(editable=True)
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def install(self, store_name:str):
        "Install This Plugin To A Store : [store_name]."
        store = Store.objects.get(name=store_name)
        store.plugins.add(self)
        store.Attrs.integrations.append(self)

    def uninstall(self, store_name:str):
        "Uninstall This Plugin To A Store : [store_name]."
        store = Store.objects.get(name=store_name)
        store.plugins.remove(self)
        store.Attrs.integrations.remove(self)

    def has_perm(self, perm, store_name):
        if perm in list(self.permissions.all()):
            if perm.granted(store_name):
                return True
            return False
        return False


# Install Default Plugins to a store
#  when it is newly created
# 
@receiver(signal=[post_save], sender='store.Store')
def install_default_plugins(sender, **kwargs):
    "Installs the default plugins to a store"
    plugins = list(Plugin.objects.filter(ours=True))
    store = Store.objects.get(name=kwargs.get('instance').name)
    store.Attrs.integrations.extend(plugins)
    return True

class Permission(models.Model):
    name = models.CharField(max_length=50)
    plugins = models.ManyToManyField('Plugin', blank=True)
    stores_granted = models.ManyToManyField('store.Store', blank=True)
    verbose_name = models.CharField(max_length=300)
    
    def granted(self, store_name:str):
        stores = list(self.stores_granted.all())
        if store_name in stores:
            return True
        return False

    def __str__(self):
        return self.verbose_name
