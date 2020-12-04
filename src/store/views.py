import os
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher, pbkdf2
from datetime import datetime
from django.conf import settings
from django.views.generic import ListView, DetailView
from gateways.payment import vougePay
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


#::::::::::::::::::::: Globals :::::::::::::::::::::::::::::::::::

# retieves user's cart
def  getCart(request, slug):
    store = Store.objects.get(slug=slug)
    if not request.user.is_authenticated:
        sessionid = request.session._get_session_key()
        user = User(userslug=sessionid)
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




# retrieves user's wishlist
def getWish(request, slug):
    store = Store.objects.get(slug=slug)
    if not request.user.is_authenticated:
        sessionid = request.session._get_session_key()
        user = User(userslug=sessionid)
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


# Generates an Invoice when the chekout view loads
def makeInvoice(request, cart:Cart, store:Store):
    done = True
    num = ''
    # expired = Invoice.objects.filter(issuer=Store.id).filter(status='pending')
    # print("OLD INVOICES : ", expired)
    # for i in expired.all():
    #     i.delete()
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

# Closed View [redirect to this view only when store's closed]

def closed_view(request, slug):
    store = Store.objects.get(slug=slug)
    if not store.is_open:   # show this page else go to store
        template = '%s/closed.html' % store.template_dir
        context = {
            'store': store,
        }
        return render(request, template, context)
        
    return redirect('store:store-view', slug)

#+++++++++++++++++++++++ Store Views ++++++++++++++++++++++++++++++

# Store View
def store_view(request, slug):
    store = Store.objects.get(slug=slug)
    if not store.is_open:
        return redirect('store:closed', slug)
    cart = getCart(request, slug)
    wish = getWish(request, slug)
    products = store.products.all().order_by('-id')
    template = '%s/home-page.html' % store.template_dir
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
        'wish': wish,
        'has_account': has_account,
    }
    return render(request, template, context)


# Cart View
def cart_view(request, slug, *args, **kwargs):
    user = request.user
    store = Store.objects.get(slug=slug)
    if not store.is_open:
        return redirect('store:closed', slug)
    cart = getCart(request, slug)
    wish = getWish(request, slug)
    items = cart.items.all().order_by('-id')
    template = '%s/cart.html' % store.template_dir
    context = {
        'title': 'Cart',
        'items': items,
        'store': store,
        'cart': cart,
        'wish': wish,
        'template': template,
    }
    return render(request, template, context)


# WishList View
def wish_view(request, slug, *args, **kwargs):
    user = request.user
    store = Store.objects.get(slug=slug)
    if not store.is_open:
        return redirect('store:closed', slug)
    wish = getWish(request, slug)
    cart = getCart(request, slug)
    items = wish.items.all()
    template = '%s/wish.html' % store.template_dir
    context = {
        'title': 'Wishlist',
        'items': items,
        'store': store,
        'wish': wish,
        'cart': cart,
        'template': template,
    }
    return render(request, template, context)


# Item Detail View
def product_view(request, slug, item_id, *args, **kwargs):
    store = Store.objects.get(slug=slug)
    if not store.is_open:
        return redirect('store:closed', slug)
    products = store.products.all()
    item = Product.objects.get(id=item_id)
    other_items = products.filter(category=item.category)
    template = '%s/product-page.html' % store.template_dir
    cart = getCart(request, slug)
    wish = getWish(request, slug)

    context = {
        'title': 'Product',
        'template': template,
        'item': item,
        'store': store,
        'other_items': other_items[:6],
        'cart': cart,
        'wish': wish,
    }
    return render(request, template, context)
def search_view(request, slug):
    store = Store.objects.get(slug=slug)
    if not store.is_open:
        return redirect('store:closed', slug)
    query = request.POST['query']
    items = []
    name_match = store.products.all().filter(name__contains=query)
    description_match = store.products.all().filter(description__contains=query)
    for i in name_match.all():
        items.append(i)
    for j in description_match.all():
        if not j in items:
            items.append(j)
    cart = getCart(request, store.slug)
    wish = getWish(request, store.slug)
    template = '%s/search-results.html' % store.template_dir
    context = {
        'title': 'Search Results',
        'template': template,
        'query': query,
        'items': items,
        'store': store,
        'cart': cart,
        'wish': wish,
    }
    return render(request, template, context)



# The checkout View
def checkout_view(request, slug):
    user = request.user
    store = Store.objects.get(slug=slug)
    if not store.is_open:
        return redirect('store:closed', slug)
    products = store.products.all()
    cart = getCart(request, store.slug)
    wish = getWish(request, store.slug)
    items = cart.items.all()
    # Generate an Invoice if this is the first time the page loads (redirects inclusive)
    invoice = makeInvoice(request, cart, store)
    if products.count() > 0:
        template = '%s/checkout-page.html' % store.template_dir
    else:
        template = '%s/test-checkout-page.html' % store.template_dir
    context = {
	'title': 'Checkout',
        'store': store,
        'cart': items,
        'wish': wish,
        'order': cart,
        'template': template,
        'invoice': invoice,
    }
    if request.method == "POST":
        gate = vougePay.Order(invoice, store.owner.merchant_id, store)
        data = request.POST        
        card = {
            'phone' : data['card_num'],
            'email' : data['card_num'],
            'card_num' : data['card_num'],
            'card_name' : data['card_name'],
            'card_exp' : data['card_exp'],
            'card_cvv' : data['card_cvv'],
        }

        ship_to = {
            'name' : data['card_num'],
            'address1' : data['address1'],
            'address2' : data['address2'],
            'country' : data['country'],
            'state' : data['state'],
        }

        return checkout(request, slug, invoice.number, gate, card, invoice.amount)

    return render(request, template, context)
    

#+++++++++++++++++++++++++ URL METHODS +++++++++++++++++++++++++++++

# checkout payment processor. This is not the checkout view!
# reacts to payment method specified during checkout.
def checkout(request, slug, invoice_num, gate, card, amt):
    "charge card -> process payment ? successful { payMerchant -> redirect shopper } : { fail -> go back }"
    res = gate.pay(card, amt)
    if res[1] == 'OK':
        messages.success(request, "Checkout Successful! Your order is being processed.")
        return redirect('store:checkout-complete', slug, invoice_num)
    else:
        messages.error(request, "Sorry, The process failed. Try Again")
        return redirect('store:checkout')


# adds an item to cart. default qty = 1
def add_to_cart(request, slug, item_id, *args, **kwargs):
    try:
        quantity = int(request.POST['quantity'])
    except:
        quantity = 1
    product = Product.objects.get(id=item_id)
    store = Store.objects.get(slug=slug)
    cart = getCart(request, slug)
    if quantity < product.quantity:
        item = CartItem(cart=cart ,item=product, quantity=quantity)
        item.save(); cart.items.add(item); cart.save()
        product.quantity -= item.quantity
        product.save()
    return redirect('store:store-view', store.slug)


# wishlist catalog
def add_to_wish(request, slug, item_id, *args, **kwargs):
    product = Product.objects.get(id=item_id)
    store = Store.objects.get(slug=slug)
    wishlist = getWish(request, slug)
    wish = WishItem(list=wishlist ,item=product)
    wish.save(); wishlist.items.add(wish); wishlist.save()
    return redirect('store:store-view', store.slug)

# remove an item from cart
def remove_wish(request, slug, item_id):
    item = WishItem.objects.get(id=item_id)
    item.delete()
    return redirect('store:wish-view', slug)

# remove an item from cart
def delete_cart_item(request, slug, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('store:cart-view', slug)


# Change the quantity of a cart item. usually > 1
def change_cart_item(request, slug, item_id):
    item = CartItem.objects.get(id=item_id)
    quantity = request.POST['quantity']
    if quantity < item.item.quantity:
        item.quantity = quantity
        item.save()
    return redirect('store:cart-view', slug)


# Increases the quantity of a cart item by 1
def increase_cart_item(request, slug, item_id):
    item = CartItem.objects.get(id=item_id)
    if item.quantity < item.item.quantity:
        item.quantity += 1
        item.save()
    return redirect('store:cart-view', slug)


# Decreases the quantity of a cart item by 1
def decrease_cart_item(request, slug, item_id):
    item = CartItem.objects.get(id=item_id)
    if not item.quantity < 1:
        item.quantity -= 1
        item.save()
    return redirect('store:cart-view', slug)


# Redeems a coupon in a store. Alters Invoice
def redeem_coupon(request, slug, invoice_num):
    store = Store.objects.get(slug=slug)
    user = request.user
    coupon_code = request.POST['coupon_code']
    coupon = Coupon.objects.filter(store=store).get(code=coupon_code)
    invoice = Invoice.objects.get(number=invoice_num)
    if not user in coupon.been_used_by.all():
        invoice.amount -= coupon.worth
        invoice.save()
        coupon.been_used_by.add(user)
        coupon.save()
    return redirect('store:checkout-view', slug)



# Post Payment Success
def on_checkout_success(request, slug, invoice_num):
    user = request.user
    store = Store.objects.get(slug=slug)
    if not user in store.customers.all():
        store.customers.add(user)
        store.save()    # save new customer to store
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
    cart.clear()    # empty cart
    return redirect('store:cart-view', store.slug)



# update user cart after every login  
# params 
# old_usr = default user instance with sessionid as email
# new_usr = authenticated user
def update(request, old_usr, new_usr, store):
    "Update cart for present user using previous session"
    old_cart = Cart.objects.filter(store=store).get(owner=old_usr)
    new_cart = getCart(request, store.slug)
    if old_cart.items.all().count() > 0:
        for item in old_cart.items.all():
            new_cart.items.add(item)
        new_cart.save()
    old_cart.clear()
    old = old_cart.owner
    old_cart.delete()
    old.delete()
    return new_cart