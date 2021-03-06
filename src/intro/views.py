from django.shortcuts import render, redirect
from store.models import Store
from django.dispatch.dispatcher import receiver



def home_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            stores = Store.objects.filter(owner=user.merchant)
            for store in stores.all():
                if store.Attrs.is_admin_logged_in == True:
                    store = store
                    return render(request, 'base/home.html', {'store': store})
        except:
            return render(request, 'base/home.html', {'store': None})
    return render(request, 'base/home.html', {'store':None})