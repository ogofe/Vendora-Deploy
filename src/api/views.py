import json
from django.shortcuts import render
from .serializers import (
    CreateStoreAPI, ReadUpdateStoreAPI,
    StoreAPI, ProductAPI, Loginizer,
    MerchantAPI, serialize_user, 
    MerchantCreateAPI,
)
from rest_framework.viewsets import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import (
    Is_Merchant, Is_Merchant_or_Staff,    
)
from store.models import (
    Store, Currency,
    Product, CartItem,
)
from accounts.models import Merchant
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate




@api_view(["GET"])
def index(request):
    """
        Vendora API Index List:\n
        **Use this url schemes to interact with the API.**\n
            Each url scheme has children endpoints that command the API.\n
            The Urls on their own are just documentation.
    """
    data = {
        '/api' : 'Show Index',
        '/api/new' : 'Show All New Urls Path',
        '/api/auth' : 'Show Auth Urls',
        '/api/pay' : 'Show Payment Urls',
    }
    return Response(data=data)


@api_view(["GET"])
def index_new(request):
    """
        Vendora API Index List [NEW]:\n
        **Use this url scheme to interact with the API new Endpoints.**\n
            Each Endpoint creates a new model instance. Never send GET requests here.\n
            Refer back to "https://readthedocs.io/vendora-api" for more info.
    """
    data = {
        'new/user' : 'Create a new user / sign up',
        'new/merchant' : 'Create a new merchant with logged in user',
        'new/store' : 'Open a new store',
        'new/item/<store_name>' : 'Add a new product to a store',
    }
    return Response(data=data)

    
    
#               ENDPOINT '/new/'

class CreateNewStore(generics.CreateAPIView):
    """
    **Open a new store**.\n
        Required Fields:\n
            Owner :: This argument is supplied automatically.\n
            Name  :: The name of the new store.\n
            Currency :: The desired currency of the new store.\n
                NOTE :: This will be the currency products and orders are charged in.
    """
    permission_classes = [Is_Merchant]
    serializer_class = CreateStoreAPI
    model = Store

    def post(self, request, *args, **kwargs):
        "Override post to save with current merchant instance."
        data = self.request.POST
        merchant = self.request.user.merchant
        store = Store(
            name = data['name'],
            owner = merchant,
            currency = Currency.objects.get(id=data['currency']),
            template_dir = data['template_dir']
        )
        store.save(); merchant.stores.add(store)
        merchant.save(); store.setup()
        try:
            store.logo = data['logo']
            store.save()
        except: #no image provided:
            pass
        return Response(data={'Task Successful': "%s was successfully created." % data['name']})
        # return Response(data={'Task Failed': "An error occured while trying to create %s." % data['name']})
    

#           Store admin views

class StoreBackendView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreAPI
    lookup_field = 'slug'
        
    permission_classes = [IsAuthenticated, Is_Merchant_or_Staff]

    # def get_object(self):
    #     name = self.kwargs.get('slug')
    #     return Store.objects.get(slug=slug)
    

class MerchantCreateView(generics.CreateAPIView):
    model = Merchant
    serializer_class = MerchantCreateAPI
    lookup_field = 'id'
    
    # def get_object(self, queryset):
        
    permission_classes = [IsAuthenticated]
    
    

class MerchantView(generics.RetrieveAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantAPI
    lookup_field = 'id'
    
    # def get_object(self, queryset):
        
    permission_classes = [IsAuthenticated, Is_Merchant_or_Staff]
    
    
    
# For Store Frontend
class StoreFrontView(generics.ListAPIView):
    """
        ** A Basic Store View On Entry. **\n
            Provides all Info of items in a store.
    """
    serializer_class = ProductAPI
    lookup_field = 'store'
    
    def get_queryset(self, *args, **kwargs):
        store = Store.objects.get(slug=self.kwargs['store'])
        queryset = Product.objects.filter(store=store)
        return queryset
    
    
    
# Auth Views
class LoginView(generics.GenericAPIView):
    serializer_class = Loginizer
    allowed_methods = ["POST"]
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        data = request.data
        uname = data['username']
        pswd = data['password']        
        try:
            user = authenticate(self.request, username=uname, password=pswd)
            if user:
                print("USER : ", user)
                login(self.request, user)
                info = 'You are now logged in as %s' % user
                code = 200
                # user = serialize(user) 
                user = serialize_user(user) 
                return Response(data={'Info': '%s' % info, 'code': code})
                return Response(data={'Info': '%s' % info, 'code': code, 'user': user}) # serialize needed
            else:
                info = 'Authentication Failed.'
                code = 404
                return Response(data={'Info': '%s' % info, 'code': code})
                
        except expression as identifier:
            info = 'Authentication Failed.'
            code = 404
            return Response(data={'Info': '%s' % info, 'code': code})


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response(data={'Info': 'You need to login to access the API'})
