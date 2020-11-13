from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from store.models import Store, Currency
from vendor.models import Alert
from django.contrib import messages
from django.conf import settings
from accounts.models import User, BillingAddress
from store.views import update

# User = settings.AUTH_USER_MODEL

def signup_view(request):
    if request.method == "POST":
        data = request.POST
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
        )
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user.save_base()
        if password1 and password2 and password2 == password1:
            user.set_password(password1)
        user.save()
        logout(request)
        login(request, user)
        name= request.POST['store_name']
        store = Store(name=name, owner=user)
        store.save()
        return redirect('accounts:personalize', store.name)
    context = {
        'idx': 0,
        'store': False,
    }
    return render(request, 'admin/auth/sign-up.html', context)

def personalize(request, store_name):
    store = Store.objects.get(name=store_name)
    store.Attrs.is_admin_logged_in = True
    if request.method == 'POST':
        currency = Currency.objects.get(code=request.POST['currency'])
        store.currency = currency
        if request.POST.get('template'):
            store.Attrs.template = request.POST['template']
        store.save()
        return redirect('accounts:billing', store.name)
    context = {
        'idx':1,    # page index
        'currencies': Currency.objects.all(),
        'store': store,
    }
    return render(request, 'admin/auth/sign-up.html', context)

def billing(request, store_name):
    store = Store.objects.get(name=store_name)
    store.Attrs.is_admin_logged_in = True
    if request.method == 'POST':
        data = request.POST
        bill = BillingAddress(
            user=request.user,
            country= data['country'],
            state=data['state'],
            city=data['city'],
            address=data['address'],
            card_name=data['card_name'],
            card_number=data['card_number'],
            card_cvv=data['card_cvv'],
            card_exp=data['card_exp']
            )
        if data.get('opt_address'):
            bill.opt_address=data['address']
        bill.save()
        return redirect('vendor:store', store_name)
    context = {
        'idx':2,    # page index
        'currencies': Currency.objects.all(),
        'store': store,
    }
    return render(request, 'admin/auth/sign-up.html', context)

def skip_to_free(request, store_name):
    msg = """
    You have not set billing on your store, you are on free trial.
    Your free trial ends in 7 days after which your store will be deactivated.
    <a href="{% url 'accounts:billing' store.name %}" class="btn btn-sm green white-text">Setup Billing Now</a> to prevent this.
    """
    store = Store.objects.get(name=store_name)
    alert = Alert(
        priority=1,
        message=msg,
        title='Billing is not saved',
        store=store,
        maker="Vendora Bot"
    )
    alert.save()
    return redirect('vendor:store', store.name)

# Log Into Store Admin
def login_view(request):
    if request.method == 'POST':
        store_name = request.POST['username']
        password = request.POST['password']
        try:     # check if store exists
            store = Store.objects.get(name=store_name) # get the store by the name requested
            if store: # store exists? Yes
                owner = User.objects.get(email=store.owner.email) # get the store owner's user
                user = authenticate(request, email=owner.email, password=password)
                if user:
                    login(request, user)
                    return redirect('vendor:dashboard', store_name)
                else:
                    messages.error(request, 'The Store Name or Password Is Incorrect!')
                    return render(request, 'admin/auth/login.html', {})
            else:
                messages.error(request, 'The Store does not exist!')
                return render(request, 'admin/auth/login.html', {})
        except: # store doesn't exist
            messages.error(request, 'The Store does not exist!')
            return render(request, 'admin/auth/login.html', {})
    return render(request, 'admin/auth/login.html')



# unauthorized access, mostly from url pasting
def error503(request):
    return render(request, 'errors/503.html', {})

def logout_view(request):
    logout(request)
    return redirect('base:home')

#+++++++++++ STORE LOGIN VIEW (AS A SHOPPER) ++++++++++++++++++===

def store_login_view(request, store_name):
    store = Store.objects.get(name=store_name)
    default_user = request.user
    props = {
        'store' : store,
    }
    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data['email'], password=data['password'])
        if user:
            if not user in store.customers.all():
                messages.error(request, "You don't have an account with this store.\n Sign up Instead.")
                return render(request, 'admin/auth/store-login.html', props)
            else:
                login(request, user)
                update(default_user, user, store)
                return redirect('store:store-view', store_name)
        else:
            messages.error(request, "You don't have an account with this store.\n <br> Sign up Instead.")
            return render(request, 'admin/auth/store-login.html', props)

    return render(request, 'admin/auth/store-login.html', props)
