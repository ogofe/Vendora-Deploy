from django.urls import path
from .views import (
    dashboard_view, is_store_owner, logout_view,
    store_view, delete_product, close_store,
    open_store, add_item_view, create_product,
    customers_view, alerts_view, integrations_view,
    reports_view, export_contacts, edit_store_view,
    close_alert, settings_view,
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

    #+++++++++++ URL Methods ++++++++++++++++++++
    path('item/<int:item_id>/delete/', delete_product, name='delete-product'),
    path('action/close/', close_store, name='close'),
    path('action/close/', close_store, name='close'),
    path('action/alert/<int:alert_id>/delete/', close_alert, name='close-alert'),
    path('action/open/', open_store, name='open'),
    path('action/create-product/', create_product, name='create-product'),
    path('checks/', is_store_owner, name='checks'),
    path('logout/', logout_view, name='logout'),

    #+=========== Exports URLS ====================
    path('export/contacts', export_contacts, name="export-contacts"),
]
