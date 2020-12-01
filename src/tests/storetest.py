from django.test import TestCase
from .models import Store, Currency
from accounts.models import Merchant


# Create your tests here.
class Tester(TestCase):
    def setUp(self):
        self.store = Store.objects.get(name='Hodu')
    
    def test_if_store_is_open(self):
        self.assertEqual(self.store.is_open, True)