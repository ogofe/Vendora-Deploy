from django.urls import path
from store.views import (
    product_view, store_view, cart_view,
    checkout_view, add_to_cart, redeem_coupon,
    on_checkout_success, increase_cart_item,
    decrease_cart_item, change_cart_item, 
    search_view, add_to_wish, remove_wish,
    delete_cart_item, wish_view, checkout,
    closed_view,
)

# Url routing namespace dependency
app_name = 'store'

urlpatterns = [
    path('<slug>/', store_view, name='store-view'),
    path('<slug>/find/', search_view, name='search-view'),
    path('<slug>/item/<int:item_id>/', product_view, name='item-view'),
    path('<slug>/cart/', cart_view, name='cart-view'),
    path('<slug>/wish/', wish_view, name='wish-view'),
    path('<slug>/checkout/', checkout_view, name='checkout-view'),
    path('<slug>/we-are-closed/', closed_view, name='closed'),

    #+++++++++++++++ URL Methods +++++++++++++++++++

    path('<slug>/cart/item/<int:item_id>/remove/', delete_cart_item, name='delete-cart-item'),
    path('<slug>/cart/item/<int:item_id>/change/', change_cart_item, name='change-cart-quantity'),
    path('<slug>/cart/item/<int:item_id>/add/', increase_cart_item, name='plus'),
    path('<slug>/cart/item/<int:item_id>/minus/', decrease_cart_item, name='minus'),
    path('<slug>/checkout/<invoice_num>/coupon/redeem/', redeem_coupon, name='redeem-coupon'),
    path('<slug>/item/<int:item_id>/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('<slug>/item/<int:item_id>/add-to-wish/', add_to_wish, name='add-to-wish'),
    path('<slug>/wish/<int:item_id>/remove/', remove_wish, name='remove-wish'),
    path('<slug>/checkout/complete/<invoice_num>/', checkout, name='pay'),
    path('<slug>/checkout/success/<int:invoice_num>/', on_checkout_success, name='checkout-complete'),
]
