from django.test import TestCase
from .models import Store, Currency
from accounts.models import Merchant, User


# Create your tests here.
class Tester(TestCase):
    def setUp(self):
        self.user = User(username='joel', password='nothingatall')
        self.user.save()
        self.owner = Merchant.objects.create(
            profile=self.user, merchant_id='1222', phone='092478868342',
            country='Nigeria', bank_name='PLC', bank_acct_name='My Name', bank_acct_num='00129037893'
            )
        self.owner.save()
        self.cur = Currency(code='USD', symbol='$')
        self.cur.save()
        self.store = Store(name='Tester', owner=self.owner, currency=self.cur, is_open=False)
        self.store.save()
    
    def test_if_store_is_open(self):
        self.assertEqual(self.store.is_open, True)
        
    def test_closed_store_view(self, request):
        