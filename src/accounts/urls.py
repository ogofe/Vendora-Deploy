from django.urls import path
from accounts.views import (
    error503, store_login_view, logout_view,
    signup_view, personalize, skip_to_free,
    billing, login_view, create_merchant,
    create_user, errorNoNet, store_signup_view,
)


app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('create/store/', create_user, name='create-user'),
    path('create/<slug>/continue/<country>/<currency>/', create_merchant, name='create-merchant'),
    path('signup/store/<slug>/personalize', personalize, name='personalize'),
    path('signup/store/<slug>/billing', billing, name='billing'),
    path('signup/store/<slug>/skip-to-trial', skip_to_free, name='free-trial'),
    path('login/', login_view, name='login'),
    
    path('logout/', logout_view, name='logout'),
    path('error/503/', error503, name='error_503'),
    path('error/signup/failed/', errorNoNet, name='error-noNet'),
    #           Storefront urls
    path('<slug>/signup/', store_signup_view, name='store-signup'),
    path('<slug>/login/', store_login_view, name='store-login'),
]

