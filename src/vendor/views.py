import csv
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect, HttpResponsePermanentRedirect
from store.models import (
    Store, Invoice, PaymentMethod,
    Category, Coupon, Tag, Product,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from datetime import datetime
from vendor.models import Alert




def is_staff(request, store_name):
    """Checks the owner or staffs of a store and redirects 
    to the appropriate store. Handy for url pasting"""
    store = Store.objects.get(name=store_name)
    user = request.user
    try:    # is this user the store's owner?
        other_stores = Store.objects.all().filter(owner=user.merchant)
        if store.owner == user.merchant:
            store.Attrs.is_admin_logged_in = True
            for i in other_stores.all():
                i.Attrs.is_admin_logged_in = False
            return True
        elif user in store.staff_accounts.all():
            return True
        return False
    except: # or a staff?
        if store.is_staff(user):
            return True
        else:
            return False
    else:
        return False    # Breach!
    


@login_required(login_url='accounts:login')
def dashboard_view(request, store_name):
    store = Store.objects.get(name=store_name)
    if not is_staff(request, store.name):
        return redirect('accounts:error_503')
    # if not store.Attrs.is_admin_logged_in:
    #     return redirect('accounts:error_503')
    context = {
        'store': store,
    }
    
    return render(request, 'admin/store/dashboard.html', context)


@login_required(login_url='accounts:login')
def store_view(request, store_name):
    if not is_staff(request, store_name):
        return redirect('accounts:error_503')
    store = Store.objects.get(name=store_name)
    items = store.products.all().order_by('-id')
    context = {
        'title': 'Store',
        'store': store,
        'items': items,
    }
    return render(request, 'admin/store/store.html', context)



@login_required(login_url='accounts:login')
def edit_store_view(request, store_name):
    if not is_staff(request, store_name):
        return redirect('accounts:error_503')
    store = Store.objects.get(name=store_name)
    items = store.products.all()
    context = {
        'title': 'Store',
        'store': store,
    }
    return render(request, 'admin/store/edit-store.html', context)


@login_required(login_url='accounts:login')
def add_item_view(request, store_name):
    if not is_staff(request, store_name):
        return redirect('accounts:error_503')
    store = Store.objects.get(name=store_name)
    
    context = {
        'store': store,
        'tags': Tag.objects.all(),
        'cats': Category.objects.all(),
    }
    return render(request, 'admin/store/add-item.html', context)

@login_required(login_url='accounts:login')
def customers_view(request, store_name):
    if not is_staff(request, store_name):
        return redirect('accounts:error_503')
    user = request.user
    store = Store.objects.get(name=store_name)
    customers = store.customers.all()
    context = {
        'store': store,
        'customers': customers,
    }
    return render(request, 'admin/store/customers.html', context)

@login_required(login_url='accounts:login')
def alerts_view(request, store_name):
    if not is_staff(request, store_name):
        return redirect('accounts:error_503')
    store = Store.objects.get(name=store_name)
    alerts = Alert.objects.filter(store=store).order_by('-date')
    customers = store.customers.all()
    context = {
        'store': store,
        'alerts':alerts,
    }
    return render(request, 'admin/store/alerts.html', context)

@login_required(login_url='accounts:login')
def reports_view(request, store_name):
    if not is_staff(request, store_name):
        return redirect('accounts:error_503')
    store = Store.objects.get(name=store_name)
    invoices = Invoice.objects.filter(issuer=store).all()
    coupons = Coupon.objects.filter(store=store).all()
    context = {
        'store': store,
        'coupons': coupons,
        'invoices': invoices,
    }
    return render(request, 'admin/store/reports.html', context)

@login_required(login_url='accounts:login')
def integrations_view(request, store_name):
    if not is_staff(request, store_name):
        return redirect('accounts:error_503')
    store = Store.objects.get(name=store_name)
    ours = []
    others = []
    socials = []
    for plugin in store.plugins.all():
        if plugin.ours:
            ours.append(plugin)
        else:
            others.append(plugin)

    for platform in store.platforms.all():
        socials.append(platform)
    context = {
        'store': store,
        'ours': ours,
        'others': others,
        'socials': socials,
    }
    return render(request, 'admin/store/integrations.html', context)


# the settings view (will be embedded in an iframe)

def settings_view(request, store_name):
    store = Store.objects.get(name=store_name)
    context = {
        'store' : store,
    }
    return render(request, 'admin/store/settings.html', context)

#+++++++++++++++++++++ < Exports Views > ++++++++++++++++++++
#   Exports contacts and reports to spreadsheets
class CSVWriter:
    """A sample csv writer derived from django docs example.
        Implements Only the write method
    """
    def write(self, data):
        "Writes to the file by returning the data rather than storing in a buffer <- Django Docs "
        return data

def export_contacts(request, store_name:str, name=None):
    """A view that streams a large CSV file. <- Django Docs"""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet applications.
    # contact_list = request.POST.copy().pop('csrfmiddlewaretoken') # returns a list
    contact_list = request.POST.getlist('email') # returns a list of values wih key "email"
    if not name:
        name = f'{store_name.lower()}_contacts_{datetime.now().date()}' # use the date and store name if no name is provided
    pseudo_buffer = CSVWriter()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow([con]) for con in contact_list), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(name)
    return response

#+++++++++++++++++++++ </ Exports Views > ++++++++++++++++++++++


#++++++++++++++++++++++++ URL METHODS +++++++++++++++++++++
@login_required(login_url='accounts:login')
def create_product(request, store_name):
    user = request.user
    data = request.POST; image = request.FILES['image']
    store = Store.objects.get(name=store_name)
    product = Product(
        name=data['name'],
        price=data['price'],
        quantity=data['quantity'],
        image=image,
        category=Category.objects.get(name=data['cat']),
        store=store,
    )
    product.save_base()
    if data['discount']:
        product.discount_price = data['discount']
    if data['description']:
        product.description = data['description']
    if request.POST.get('sub_cats'):
        product.sub_cats.add(Category.objects.get(name=data['sub_cats']).id)
    if request.POST.get('tags'):
        product.tags.add(Tag.objects.get(name=data['tags']).id)
    product.save()
    store.products.add(product)
    store.save()
    return redirect('vendor:store', store_name)


@login_required(login_url='accounts:login')
def edit_product(request, store_name, item_id):
    store = Store.objects.get(name=store_name)
    item = Product.objects.get(id=item_id)
    cats = Category.objects.all()
    tags = Tag.objects.all()
    if request.method == 'POST':
        files = request.FILES
        data = request.POST
        item.name = data['name']; item.price = data['price']
        item.quantity = data['quantity']
        if data['discount']:
            item.discount_price = data['discount']
        if data['description']:
            item.description = data['description']
        if request.POST.get('sub_cats'):
            product.sub_cats.add(Category.objects.get(name=data['sub_cats']).id)
        if request.POST.get('tags'):
            product.tags.add(Tag.objects.get(name=data['tags']).id)
        try:
            if files['image']:
                item.image = files['image']
        except:
            pass
        item.save()
        return redirect('vendor:store', store_name)
    context = {
        'store': store,
        'item' : item,
        'cats' : cats,
        'tags' : tags,
    }
    return render(request, 'admin/store/edit-item.html', context)

@login_required(login_url='accounts:login')
def create_coupon(request, store_name):
    store = Store.objects.get(name=store_name)
    data = request.POST
    coupon = Coupon(worth=data['worth'], store=store, code= str(data['code']).upper())
    try:
        expires = data['validity']
        if expires:
            coupon.validity = expires
    except:
        pass
    coupon.save()
    store.coupons.add(coupon)
    return redirect('vendor:store', store_name)


@login_required(login_url='accounts:login')
def close_store(request, store_name):
    store = Store.objects.get(name=store_name)
    store.is_open = False; store.save()
    return redirect('vendor:store', store_name)

@login_required(login_url='accounts:login')
def close_alert(request, store_name, alert_id):
    alert = Alert.objects.get(id=alert_id)
    alert.delete()
    return redirect('vendor:alerts', store_name = alert.store)

@login_required(login_url='accounts:login')
def open_store(request, store_name):
    store = Store.objects.get(name=store_name)
    store.is_open = True; store.save()
    return redirect('vendor:store', store_name)


@login_required(login_url='accounts:login')
def delete_product(request, store_name, item_id):
    item = Product.objects.get(id=item_id)
    item.delete()
    return redirect('vendor:store', store_name)


def logout_view(request, store_name):
    store = Store.objects.get(name=store_name)
    store.Attrs.is_admin_logged_in = False
    logout(request)
    return redirect('base:home')

