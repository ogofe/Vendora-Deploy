from django.urls import path
from .views import (
    dashboard_view, is_staff, logout_view,
    store_view, delete_product, close_store,
    open_store, add_item_view, create_product,
    customers_view, alerts_view, integrations_view,
    reports_view, export_contacts, edit_store_view,
    close_alert, settings_view, create_coupon,
    edit_product, alert_action,
)

app_name = 'vendor'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('store/', store_view, name='store'),
    path('store/change/', edit_store_view, name='edit-store'),
    path('customers/', customers_view, name='customers'),
    path('alerts/', alerts_view, name='alerts'),
    path('integrations/', integrations_view, name='integrations'),
    path('reports/', reports_view, name='reports'),
    path('settings/', settings_view, name='settings'),
    path('store/new-item/', add_item_view, name='add-item'),
    path('store/edit-item/<int:item_id>/', edit_product, name='edit-item'),

    #+++++++++++ URL Methods ++++++++++++++++++++
    path('item/<int:item_id>/delete/', delete_product, name='delete-product'),
    path('action/close/', close_store, name='close'),
    path('action/close/', close_store, name='close'),
    path('action/alert/', alert_action, name='alert-action'),
    # path('action/alert/delete/', close_alert, name='close-alert'),
    path('action/create/coupon/', create_coupon, name='add-coupon'),
    path('action/open/', open_store, name='open'),
    path('action/create-product/', create_product, name='create-product'),
    path('checks/', is_staff, name='checks'),
    path('logout/', logout_view, name='logout'),

    #+=========== Exports URLS ====================
    path('export/contacts', export_contacts, name="export-contacts"),
]
