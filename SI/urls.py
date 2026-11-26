from django.urls import path

from .views import (
    create_supplier,
    edit_supplier,
    delete_supplier,
    create_buyer,
    edit_buyer,
    delete_buyer,
    create_season,
    edit_season,
    delete_season,
    create_drop,
    edit_drop,
    delete_drop,
    create_product,
    edit_product,
    delete_product,
    create_order,
    edit_order,
    update_order_status,
    delete_order,
    create_delivery,
    edit_delivery,
    delete_delivery,
    SupplierListView,
    BuyerListView,
    SeasonListView,
    DropListView,
    ProductListView,
    OrderListView,
    DeliveryListView,
)

urlpatterns = [
    path('create-supplier/', create_supplier, name='create-supplier'),
    path('supplier/<int:pk>/edit/', edit_supplier, name='edit-supplier'),
    path('supplier/<int:pk>/delete/', delete_supplier, name='delete-supplier'),

    path('create-buyer/', create_buyer, name='create-buyer'),
    path('buyer/<int:pk>/edit/', edit_buyer, name='edit-buyer'),
    path('buyer/<int:pk>/delete/', delete_buyer, name='delete-buyer'),

    path('create-season/', create_season, name='create-season'),
    path('season/<int:pk>/edit/', edit_season, name='edit-season'),
    path('season/<int:pk>/delete/', delete_season, name='delete-season'),

    path('create-drop/', create_drop, name='create-drop'),
    path('drop/<int:pk>/edit/', edit_drop, name='edit-drop'),
    path('drop/<int:pk>/delete/', delete_drop, name='delete-drop'),

    path('create-product/', create_product, name='create-product'),
    path('product/<int:pk>/edit/', edit_product, name='edit-product'),
    path('product/<int:pk>/delete/', delete_product, name='delete-product'),

    path('create-order/', create_order, name='create-order'),
    path('order/<int:pk>/edit/', edit_order, name='edit-order'),
    path('order/<int:pk>/status/', update_order_status, name='update-order-status'),
    path('order/<int:pk>/delete/', delete_order, name='delete-order'),

    path('create-delivery/', create_delivery, name='create-delivery'),
    path('delivery/<int:pk>/edit/', edit_delivery, name='edit-delivery'),
    path('delivery/<int:pk>/delete/', delete_delivery, name='delete-delivery'),

    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('buyer-list/', BuyerListView.as_view(), name='buyer-list'),
    path('season-list/', SeasonListView.as_view(), name='season-list'),
    path('drop-list/', DropListView.as_view(), name='drop-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
]
