from store.models import Store, Product, Invoice, Tag, Category, Currency
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from accounts.models import Merchant, BillingAddress, ShippingAddress
from rest_framework.fields import MultipleChoiceField


#           Serializers


class CreateUserAPI(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')



class UserAPI(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        
        

class MerchantAPI(ModelSerializer):
    profile = UserAPI()
    class Meta:
        model = Merchant
        fields = ('profile', 'merchant_id', 'phone', 'country', 'name',
                  'bank_name', 'bank_acct_name', 'bank_acct_num')
        
        
class CurrencyAPI(ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'symbol') 


class CategoryAPI(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',) 



class CategoriesAPI(ModelSerializer):
    class Meta:
        model = Category
        many = True
        fields = ('name',) 


class TagAPI(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class CreateStoreAPI(ModelSerializer):
    owner = Merchant
    class Meta:
        model = Store
        fields = ('owner', 'name', 'currency', 'logo', 'template_dir')


class StoreAPI(ModelSerializer):
    owner = MerchantAPI()
    staff_accounts = [UserAPI()]
    currency = CurrencyAPI()
    class Meta:
        model = Store
        fields ='__all__'
        lookup_field = 'name'      
        

class ReadUpdateStoreAPI(ModelSerializer):
    owner = MerchantAPI()
    staff_accounts = [UserAPI()]
    class Meta:
        model = Store
        fields = '__all__'
        
        
class ProductAPI(ModelSerializer):
    store = StoreAPI()
    tags = TagAPI()
    category = CategoryAPI()
    sub_cats = CategoriesAPI()
    class Meta:
        model = Product
        fields = ('name', 'store', 'price', 'discount_price', 'image', 'quantity', 'description', 'tags', 'category', 'sub_cats',)
        
        lookup_field = 'id'
        

class Loginizer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        
        


        
        
# class MerchantAPI(ModelSerializer):
#     class Meta:
#         model = Merchant
#         fields = '__all__'
        
        
# def serialize(obj:object) -> object:
#     "returns a JSON Serializable object "
#     new = {}
#     for field in obj.__dict__:
#         new.update(str(field), obj['field'])
#     return new


def serialize_user(user:object) -> object:
    "returns a JSON Serializable User object "
    user = {
        'firstname': user.first_name,
        'lastname': user.last_name,
        'username': user.username,
        'email': user.email,
    }
    
    