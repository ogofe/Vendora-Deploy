import os
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher, pbkdf2
from datetime import datetime
from django.conf import settings
from django.views.generic import ListView, DetailView
from store.models import (
    Store, Product,
    Cart, CartItem,
    Invoice, PaymentMethod,
    Coupon, WishList,
    WishItem,
)
from django.contrib import messages
from random import randint
from django.core.paginator import Paginator
from accounts.models import User

BASE_DIR = settings.BASE_DIR
# User = settings.AUTH_USER_MODEL



def  getCart(request, store_name):
    store = Store.objects.get(name=store_name)
    if not request.user.is_authenticated:
        sessionid = request.session._get_session_key()
        user = User(email=sessionid)
        user.set_unusable_password()
        user.save()
        login(request, user)
    try:    # if a user is logged into a store, get his/her cart
        cart = Cart.objects.filter(store=store).get(owner=request.user)
        return cart
    except: # user does not have a cart in this store
        cart = Cart(owner=request.user, store=store)
        cart.save()
        return cart

def getWish(request, store_name):
    store = Store.objects.get(name=store_name)
    if not request.user.is_authenticated:
        sessionid = request.session._get_session_key()
        user = User(email=sessionid)
        user.set_unusable_password()
        user.save()
        login(request, user)
    try:    # if a user is logged into a store, get his/her cart
        wish = WishList.objects.filter(store=store).get(owner=request.user)
        return wish
    except: # user does not have a cart in this store
        wish = WishList(owner=request.user, store=store)
        wish.save()
        return wish


def makeInvoice(request, cart:Cart, store:Store):
    done = True
    num = ''
    invoice = Invoice(amount=cart.total(), issuer=store, cart=cart, payer=request.user)
    while done:
        for i in range(0, 11):
            num += str(randint(0, 9))
        try:    # check if an invoice with this number exists
            if not Invoice.objects.get(number=num):
                invoice.number = int(num)
                invoice.save()
                done = False
                break
        except: # invoice does not exist
            invoice.number = int(num)
            invoice.save()
            done = False
            break
    return invoice


#++++++++++++++++++++++ Auth Views ++++++++++++++++++++++++++++++++
def register(request, store_name):
    data = request.POST
    store = Store.objects.get(name=store_name)
    password1 = data['password1']; password2 = data['password2']
    if password1 and password2 and password2 == password1:
        password = pbkdf2(password1.encode(), 'Kw112jkjs7873bk', 150000, 6)
    user = User(
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        password = password,
    )
    store.customers.add(user)
    return redirect('store:store-view', store_name)


#+++++++++++++++++++++++ Store Views ++++++++++++++++++++++++++++++


def store_view(request, store_name):
    store = Store.objects.get(name=store_name)
    cart = getCart(request, store_name)
    products = store.products.all().order_by('-id')
    if products.count() > 0:
        template = '%s/home-page.html' % store.Attrs.template
    else:
        template = '%s/test-home-page.html' % store.Attrs.template
    pages = Paginator(products, 100, 0)
    page = request.GET.get('page')
    items = pages.get_page(page)
    test = range(0, 8)
    if not store.owner == request.user:
        if request.user in store.customers.all():
            has_account = True
        has_account = False
    else:
        has_account = True
    context = {
        'title': 'Home',
        'items': items,
        'pages': pages,
        'store': store,
        'template': template,
        'test': test,
        'cart': cart,
        'has_account': has_account,
    }
    return render(request, template, context)

def cart_view(request, store_name, *args, **kwargs):
    user = request.user
    store = Store.objects.get(name=store_name)
    cart = getCart(request, store_name)
    items = cart.items.all().order_by('-id')
    template = '%s/cart.html' % store.Attrs.template
    context = {
        'title': 'Cart',
        'items': items,
        'store': store,
        'cart': cart,
        'template': template,
    }
    return render(request, template, context)

def wish_view(request, store_name, *args, **kwargs):
    user = request.user
    store = Store.objects.get(name=store_name)
    wish = getCart(request, store_name)
    cart = getCart(request, store_name)
    items = wish.items.all()
    template = '%s/cart.html' % store.Attrs.template
    context = {
        'title': 'Wishlist',
        'items': items,
        'store': store,
        'wish': wish,
        'cart': cart,
        'template': template,
    }
    return render(request, template, context)

def product_view(request, store_name, item_id, *args, **kwargs):
    store = Store.objects.get(name=store_name)
    products = store.products.all()
    item = Product.objects.get(id=item_id)
    other_items = products.filter(category=item.category)
    template = '%s/product-page.html' % store.Attrs.template
    cart = getCart(request, store_name)

    context = {
        'title': 'Product',
        'template': template,
        'item': item,
        'store': store,
        'other_items': other_items,
        'cart': cart,
    }
    return render(request, template, context)

def checkout_view(request, store_name):
    user = request.user
    store = Store.objects.get(name=store_name)
    products = store.products.all()
    cart = Cart.objects.filter(owner=request.user).get(store=store)
    items = cart.items.all()
    # Generate an Invoice if this is the first time the page loads (redirects inclusive)
    invoice = makeInvoice(request, cart, store)
        
    if products.count() > 0:
        template = '%s/checkout-page.html' % store.Attrs.template
    else:
        template = '%s/test-checkout-page.html' % store.Attrs.template
    context = {
	'title': 'Checkout',
        'store': store,
        'cart': items,
        'order': cart,
        'template': template,
        'invoice': invoice,
    }
    return render(request, template, context )
    


#+++++++++++++++++++++++++ URL METHODS +++++++++++++++++++++++++++++
def add_to_cart(request, store_name, item_id, *args, **kwargs):
    quantity = int(request.POST['quantity'])
    product = Product.objects.get(id=item_id)
    store = Store.objects.get(name=store_name)
    try:
        cart = Cart.objects.filter(owner=request.user).get(store=store)
        if   product.quantity >=1 and quantity <= product.quantity:
            item = CartItem(cart=cart ,item=product, quantity=quantity)
            item.save(); cart.items.add(item); cart.save()
    except: # Fails
        cart = Cart(owner=request.user, store=store)
        cart.save()
        if  product.quantity >=1 and quantity <= product.quantity:
            item = CartItem(cart=cart ,item=product, quantity=quantity)
            item.save(); cart.items.add(item); cart.save()
    return redirect('store:store-view', store.name)

def add_to_wish(request, store_name, item_id, *args, **kwargs):
    quantity = int(request.POST['quantity'])
    product = Product.objects.get(id=item_id)
    store = Store.objects.get(name=store_name)
    try:
        wishlist = WishList.objects.filter(owner=request.user).get(store=store)
        if   product.quantity >=1 and quantity <= product.quantity:
            wish = WishItem(cart=cart ,item=product, quantity=quantity)
            wish.save(); wishlist.items.add(wish); wishlist.save()
    except: # Fails
        cart = WishList(owner=request.user, store=store)
        cart.save()
        if  product.quantity >=1 and quantity <= product.quantity:
            wish = WishItem(cart=cart ,item=product, quantity=quantity)
            wish.save(); wishlist.items.add(wish); wishlist.save()
    return redirect('store:store-view', store.name)


def delete_cart_item(request, store_name, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('store:cart-view', store_name)


def change_cart_item(request, store_name, item_id):
    item = CartItem.objects.get(id=item_id)
    quantity = request.POST['quantity']
    if quantity < item.item.quantity:
        item.quantity = quantity
        item.save()
    return redirect('store:cart-view', store_name)


def increase_cart_item(request, store_name, item_id):
    item = CartItem.objects.get(id=item_id)
    if item.quantity < item.item.quantity:
        item.quantity += 1
        item.save()
    return redirect('store:cart-view', store_name)


def decrease_cart_item(request, store_name, item_id):
    item = CartItem.objects.get(id=item_id)
    if not item.quantity < 1:
        item.quantity -= 1
        item.save()
    return redirect('store:cart-view', store_name)

def redeem_coupon(request, store_name, invoice_num):
    store = Store.objects.get(name=store_name)
    user = request.user
    coupon_code = request.POST['coupon_code']
    coupon = Coupon.objects.filter(store=store).get(code=coupon_code)
    invoice = Invoice.objects.get(number=invoice_num)
    if not user in coupon.been_used_by.all():
        invoice.amount -= coupon.worth
        invoice.save()
        coupon.been_used_by.add(user)
        coupon.save()
    return redirect('store:checkout-view', store_name)

def on_checkout_success(request, store_name, invoice_num):
    user = request.user
    store = Store.objects.get(name=store_name)
    store.customers.add(user)
    store.save()
    invoice = Invoice.objects.get(number=invoice_num)
    invoice.date_paid = datetime.now()
    unpaid_invoices = Invoice.objects.filter(issuer=store).filter(payer=user).filter(status="pending")
    for invoice in unpaid_invoices:	# House Cleaning
    	invoice.delete()
    invoice.status='paid'; invoice.save()   # change invoice satus to paid and save.
    cart = Cart.objects.filter(owner=user).get(store=store)
    for item in cart.items.all():
        product = Product.objects.get(id=item.item.id)
        product.quantity -= item.quantity
        product.save()
    cart.clear()
    return redirect('store:cart-view', store.name)



# update user cart after every login  
# params 
# old_usr = default user instance with sessionid as email
# new_usr = authenticated user
def update(old_usr, new_usr, store):
    old_cart = Cart.objects.filter(store=store).get(owner=old_usr)
    try:    # try to get the users cart 
        new_cart = Cart.objects.filter(store=store).get(owner=new_usr)
    except: # this login session is for a newly created user with no cart
        new_cart = Cart(store=store, owner=new_usr)
        new_cart.save()
    if old_cart.items.all().count() > 0:
        for item in old_cart.items.all():
            new_cart.items.add(item)
        new_cart.save()
    return new_cart