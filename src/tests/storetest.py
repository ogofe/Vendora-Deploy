from django.test import TestCase
from store.models import Store, Currency, Product
from accounts.models import Merchant
from django.contrib.auth.models import User


# Create your tests here.
class Tester(TestCase):
    def setUp(self):
        self.user = User(first_name='John', last_name='Doe', username='username')
        self.user.set_password('passkodeforMe')
        self.user.save()
        self.merchant = Merchant(profile=self.user, phone='09023874854', country='Nigeria',
        merchant_id='223-45453', bank_acct_name='John Doe', bank_acct_num='323122123', 
        bank_name='Wells Fargo')
        self.merchant.save()
        self.cur = Currency(code='USD', symbol='$')
        self.cur.save()
        self.store = Store(name='Hodu', owner=self.merchant, currency=self.cur)
        self.store.save()
        self.store.staff_accounts.add(self.store.owner.profile)
        self.store.setup()
    
    def test_store_is_open(self):
        self.assertEqual(self.store.is_open, True)

    def test_store_has_products(self):
        self.assertTrue(Product.__class__ in self.store.products.all(), "Store Has 0 Products")

    