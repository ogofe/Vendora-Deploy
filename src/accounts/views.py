from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from store.models import Store, Currency
from vendor.models import Alert
from django.contrib import messages
from django.conf import settings
from accounts.models import Merchant, BillingAddress
from store.views import update
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gateways.payment.vougePay import Create


def namify(string:str):
    "Converts white spaces to underscores"
    name = string.replace(' ', '_')
    return name

def create_user(request, *args):
    data = request.POST
    user = User(
        username=namify(data['store_name']),
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
    return redirect('accounts:create-merchant', data['store_name'], data['country'], data['currency'])



@login_required(login_url='accounts:login')
def create_merchant(request, store_name, country, currency):
    if not request.method == "POST":
        return render(request, 'admin/auth/setup.html')
    data = request.POST   
    user = request.user
    # call the vouge API (Creates a vougePay wallet)
    merchant_id = Create(
        user.first_name,
        user.last_name,
        user.username,
        user.password[11:21],
        user.email,
        country=country,
        currency=currency
    )
    if merchant_id:
        merchant = Merchant(
            profile=user,
            merchant_id=merchant_id,
            phone=data['phone'],
            country=country,
            bank_name=data['bank_name'],
            bank_acct_name=data['bank_acct_name'],
            bank_acct_num=data['bank_acct_number'],
        )
        merchant.save()
        store = Store(name=store_name, owner=merchant)
        store.save()    
        store.setup()   # setup the store
        return redirect('accounts:billing', store.name)
    return redirect('accounts:error-noNet', store.name)

    

def signup_view(request):
    
    context = {
        'currencies': Currency.objects.all(),
        'idx': 0,
        'store': False,
    }
    return render(request, 'admin/auth/sign-up.html', context)

def personalize(request, store_name):
    store = Store.objects.get(name=store_name)
    store.Attrs.is_admin_logged_in = True
    if request.method == 'POST':
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
    Setup Billing Now to prevent this.
    """
    link = 'http://localhost:8000/%s/add/billing/' % store.name
    store = Store.objects.get(name=store_name)
    alert = Alert(
        priority=1,
        message=msg,
        title='Billing is not saved',
        store=store,
        maker="Vendora Bot",
        cta = "Setup Billing",
        cta_link=link
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
                owner = User.objects.get(email=store.owner.profile.email) # get the store owner's user
                user = authenticate(request, username=owner.username, password=password)
                if user:
                    login(request, user)
                    return redirect('vendor:dashboard', store_name)
                else:                
                    for acc in store.staff_accounts.all():
                        staff = authenticate(request, username=acc.username, password=password)
                        if staff in store.staff_accounts.all():
                            login(request, staff)
                            return redirect('vendor:dashboard', store_name)                            
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


# unauthorized access, mostly from url pasting
def errorNoNet(request):
    return render(request, 'errors/no-net.html', {})

def logout_view(request):
    logout(request)
    return redirect('base:home')

#+++++++++++ STOREFRONT LOGIN VIEW (AS A SHOPPER) ++++++++++++++++++===

def store_login_view(request, store_name):
    store = Store.objects.get(name=store_name)
    default_user = request.user
    context = {
        'store' : store,
    }
    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            if not user in store.customers.all():
                messages.error(request, "Incorrect username or password.")
                return render(request, 'admin/auth/store-login.html', context)
            else:
                login(request, user)
                if default_user.has_usable_password() == False:
                    update(request, default_user, user, store)
                return redirect('store:store-view', store_name)
        else:
            messages.error(request, "Incorrect username or password.")
            return render(request, 'admin/auth/store-login.html', context)

    return render(request, 'admin/auth/store-login.html', context)


#   Storefront signup view

def store_signup_view(request, store_name):
    store = Store.objects.get(name=store_name)
    old_user = request.user
    if request.method == 'POST':
        data = request.POST
        # create a new user and add to store's record
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['username']
        )
        if data['password1'] and data['password2'] and data['password2'] == data['password1']:
            user.set_password(data['password1'])
            user.save()
            login(request, user)
            if old_user.has_usable_password() == False:
                update(request, old_user, user, store)
            store.customers.add(user)
            store.save()
        return redirect('store:store-view', store_name)
    context = {
        'store': store,
        'title': 'Signup',
    }
    return render(request, 'admin/auth/store-signup.html', context)