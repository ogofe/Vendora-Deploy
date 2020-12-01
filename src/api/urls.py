from django.urls import path
from .views import (
    CreateNewStore, index, index_new, StoreBackendView,
    StoreFrontView, LoginView, logout_view, MerchantView,
    StoreInfoView,
)

app_name = 'api'

urlpatterns = [
    # api docs
    path('', index, name="index"),
    path('new/', index_new, name="index-new"),
    
    
    # Auth
    path('auth/logout/', logout_view, name="logout"),
    path('auth/login/', LoginView.as_view(), name="login"),

    # [Enpoints] '/new/'
    path('new/store', CreateNewStore.as_view(), name="new-store"),
    
    # Store Frontend View
    path('store/<store>/', StoreFrontView.as_view(), name='store-view'),
    
    # Backend Views
    path('<name>/', StoreInfoView.as_view(), name="store-info"),
    path('<name>/admin/', StoreBackendView.as_view(), name="store-admin"),
    path('<name>/owner/<id>', MerchantView.as_view(), name="merchant-view"),
]
