from django.urls import path
from accounts.views import (
    error503,
    store_login_view,
    logout_view,
    signup_view,
    personalize,
    skip_to_free,
    billing,
    login_view,
)


app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signup/store/<str:store_name>/personalize', personalize, name='personalize'),
    path('signup/store/<str:store_name>/billing', billing, name='billing'),
    path('signup/store/<str:store_name>/skip-to-trial', skip_to_free, name='free-trial'),
    path('login/', login_view, name='login'),
    path('<str:store_name>/login/', store_login_view, name='store-login'),
    path('logout/', logout_view, name='logout'),
    path('error/503/', error503, name='error_503'),
]

