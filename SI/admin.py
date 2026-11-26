from django.contrib import admin

from .models import (
    Supplier,
    Buyer,
    Season,
    Drop,
    Product,
    Order,
    Delivery,
)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'address', 'created_date']
    search_fields = ['name', 'address', 'user__username', 'user__email']
    list_filter = ['created_date']


class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'address', 'created_date']
    search_fields = ['name', 'address', 'user__username', 'user__email']
    list_filter = ['created_date']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sortno', 'created_date']
    search_fields = ['name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['design', 'product', 'supplier', 'buyer', 'drop', 'status', 'created_date']
    list_filter = ['status', 'season', 'drop']
    search_fields = ['design', 'color', 'product__name', 'supplier__name', 'buyer__name']


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'courier_name', 'created_date']
    search_fields = ['courier_name', 'order__design', 'order__product__name']


class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_date']
    search_fields = ['name', 'description']


class DropAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date']
    search_fields = ['name']


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Drop, DropAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Delivery, DeliveryAdmin)
