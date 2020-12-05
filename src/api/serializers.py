from store.models import Store, Product, Invoice, Tag, Category, Currency
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Merchant, BillingAddress, ShippingAddress
from rest_framework.fields import MultipleChoiceField


#           Serializers

ModelSerializer = serializers.ModelSerializer

class CreateUserAPI(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')



class UserAPI(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        
        

class MerchantCreateAPI(ModelSerializer):
    profile = User
    class Meta:
        model = Merchant
        fields = ('profile', 'merchant_id', 'phone', 'country',
                  'bank_name', 'bank_acct_name', 'bank_acct_num')
        
        
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
    staff_accounts = serializers.StringRelatedField(many=True)
    customers = User.objects.all()
    # customers = serializers.PrimaryKeyRelatedField(queryset=UserAPI())
    # customers = serializers.RelatedField(queryset=User.objects.all())
    # customers = serializers.StringRelatedField(many=True)
    products = serializers.StringRelatedField(many=True)
    plugins = serializers.StringRelatedField(many=True)
    coupons = serializers.StringRelatedField(many=True)
    currency = CurrencyAPI()
    platforms = serializers.StringRelatedField(many=True)
    payment_methods = serializers.StringRelatedField(many=True)
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
    category = CategoriesAPI()
    tags = serializers.StringRelatedField(many=True)
    sub_cats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = ('name', 'store', 'price', 'discount_price', 
                  'image', 'quantity', 'description', 'tags', 'category', 'sub_cats',)
        
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
    
    