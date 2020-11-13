from django.urls import path
from intro.views import home_view

app_name = 'base'


urlpatterns = [
    path('', home_view, name='home'), 
]
