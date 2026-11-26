from django.contrib import admin

from .models import User


@admin.action(description='Approve selected pending accounts')
def approve_selected_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_admin', 'is_supplier', 'is_buyer', 'date_joined']
    list_filter = ['is_active', 'is_admin', 'is_supplier', 'is_buyer']
    search_fields = ['username', 'email']
    actions = [approve_selected_users]


admin.site.site_header = 'PT TARINDO — Admin CMS'
admin.site.site_title = 'PT TARINDO CMS'
admin.site.index_title = 'Inventory, Partners & User Administration'
admin.site.register(User, UserAdmin)
