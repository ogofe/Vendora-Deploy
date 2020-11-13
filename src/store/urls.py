from django.urls import path
from store.views import (
    product_view, store_view, cart_view,
    checkout_view, add_to_cart, redeem_coupon,
    on_checkout_success, increase_cart_item,
    decrease_cart_item, change_cart_item,
    delete_cart_item, wish_view,
)

# Url routing namespace dependency
app_name = 'store'

urlpatterns = [
    path('<str:store_name>/', store_view, name='store-view'),
    path('<str:store_name>/item/<int:item_id>/', product_view, name='item-view'),
    path('<str:store_name>/cart/', cart_view, name='cart-view'),
    path('<str:store_name>/wish/', wish_view, name='wish-view'),
    path('<str:store_name>/checkout/', checkout_view, name='checkout-view'),

    #+++++++++++++++ URL Methods +++++++++++++++++++

    path('<str:store_name>/cart/item/<int:item_id>/remove/', delete_cart_item, name='delete-cart-item'),
    path('<str:store_name>/cart/item/<int:item_id>/change/', change_cart_item, name='change-cart-quantity'),
    path('<str:store_name>/cart/item/<int:item_id>/add/', increase_cart_item, name='plus'),
    path('<str:store_name>/cart/item/<int:item_id>/minus/', decrease_cart_item, name='minus'),
    path('<str:store_name>/checkout/<str:invoice_num>/coupon/redeem/', redeem_coupon, name='redeem-coupon'),
    path('<str:store_name>/item/<int:item_id>/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('<str:store_name>/checkout/complete/<int:invoice_num>/', on_checkout_success, name='checkout-complete'),
]
