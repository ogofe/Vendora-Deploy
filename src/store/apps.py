from django.apps import AppConfig
from django.dispatch import Signal

# Signal._live_receivers
class StoreConfig(AppConfig):
    name = 'store'

    # Overriding ready() so signals can be registered
    # as in django docs
    def ready(self):
        store = self.get_model('Store')
        for plugin in store.plugins.all():
            Signal.connect(plugin.listener, sender='store.Store')

