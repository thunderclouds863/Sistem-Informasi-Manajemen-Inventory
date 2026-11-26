from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from users.models import User
from .models import (
    Supplier,
    Buyer,
    Season,
    Drop,
    Product,
    Order,
    Delivery,
)
from .forms import (
    SupplierForm,
    SupplierEditForm,
    BuyerForm,
    BuyerEditForm,
    SeasonForm,
    DropForm,
    ProductForm,
    OrderForm,
    OrderEditForm,
    DeliveryForm,
)
from .permissions import admin_required, is_admin_user


class RoleContextMixin(LoginRequiredMixin):
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin_user'] = is_admin_user(self.request.user)
        return context


# Supplier views
@admin_required
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password != retype_password:
                forms.add_error('retype_password', 'Passwords do not match.')
            elif User.objects.filter(username=username).exists():
                forms.add_error('username', 'This username is already taken.')
            elif Supplier.objects.filter(name=name).exists():
                forms.add_error('name', 'A supplier with this name already exists.')
            else:
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            username=username, password=password,
                            email=email, is_supplier=True
                        )
                        Supplier.objects.create(user=user, name=name, address=address)
                    messages.success(request, f'Supplier "{name}" has been created.')
                    return redirect('supplier-list')
                except IntegrityError:
                    forms.add_error(None, 'Could not create supplier. Please check the entered details.')
    return render(request, 'store/create_supplier.html', {'form': forms, 'is_edit': False})


@admin_required
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier.objects.select_related('user'), pk=pk)
    initial = {
        'name': supplier.name,
        'address': supplier.address,
        'email': supplier.user.email,
    }
    forms = SupplierEditForm(initial=initial)
    if request.method == 'POST':
        forms = SupplierEditForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            if Supplier.objects.exclude(pk=supplier.pk).filter(name=name).exists():
                forms.add_error('name', 'A supplier with this name already exists.')
            else:
                with transaction.atomic():
                    supplier.name = name
                    supplier.address = address
                    supplier.save()
                    supplier.user.email = email
                    supplier.user.save(update_fields=['email'])
                messages.success(request, f'Supplier "{name}" has been updated.')
                return redirect('supplier-list')
    return render(request, 'store/create_supplier.html', {
        'form': forms,
        'is_edit': True,
        'instance': supplier,
    })


@admin_required
@require_POST
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier.objects.select_related('user'), pk=pk)
    name = supplier.name
    with transaction.atomic():
        user = supplier.user
        supplier.delete()
        user.delete()
    messages.success(request, f'Supplier "{name}" has been deleted.')
    return redirect('supplier-list')


class SupplierListView(RoleContextMixin, ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'

    def get_queryset(self):
        return Supplier.objects.select_related('user').order_by('-id')


# Buyer views
@admin_required
def create_buyer(request):
    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password != retype_password:
                forms.add_error('retype_password', 'Passwords do not match.')
            elif User.objects.filter(username=username).exists():
                forms.add_error('username', 'This username is already taken.')
            elif Buyer.objects.filter(name=name).exists():
                forms.add_error('name', 'A buyer with this name already exists.')
            else:
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            username=username, password=password,
                            email=email, is_buyer=True
                        )
                        Buyer.objects.create(user=user, name=name, address=address)
                    messages.success(request, f'Buyer "{name}" has been created.')
                    return redirect('buyer-list')
                except IntegrityError:
                    forms.add_error(None, 'Could not create buyer. Please check the entered details.')
    return render(request, 'store/create_buyer.html', {'form': forms, 'is_edit': False})


@admin_required
def edit_buyer(request, pk):
    buyer = get_object_or_404(Buyer.objects.select_related('user'), pk=pk)
    initial = {
        'name': buyer.name,
        'address': buyer.address,
        'email': buyer.user.email,
    }
    forms = BuyerEditForm(initial=initial)
    if request.method == 'POST':
        forms = BuyerEditForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            if Buyer.objects.exclude(pk=buyer.pk).filter(name=name).exists():
                forms.add_error('name', 'A buyer with this name already exists.')
            else:
                with transaction.atomic():
                    buyer.name = name
                    buyer.address = address
                    buyer.save()
                    buyer.user.email = email
                    buyer.user.save(update_fields=['email'])
                messages.success(request, f'Buyer "{name}" has been updated.')
                return redirect('buyer-list')
    return render(request, 'store/create_buyer.html', {
        'form': forms,
        'is_edit': True,
        'instance': buyer,
    })


@admin_required
@require_POST
def delete_buyer(request, pk):
    buyer = get_object_or_404(Buyer.objects.select_related('user'), pk=pk)
    name = buyer.name
    with transaction.atomic():
        user = buyer.user
        buyer.delete()
        user.delete()
    messages.success(request, f'Buyer "{name}" has been deleted.')
    return redirect('buyer-list')


class BuyerListView(RoleContextMixin, ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'

    def get_queryset(self):
        return Buyer.objects.select_related('user').order_by('-id')


# Season views
@admin_required
def create_season(request):
    forms = SeasonForm()
    if request.method == 'POST':
        forms = SeasonForm(request.POST)
        if forms.is_valid():
            season = forms.save()
            messages.success(request, f'Season "{season.name}" has been created.')
            return redirect('season-list')
    return render(request, 'store/create_season.html', {'form': forms, 'is_edit': False})


@admin_required
def edit_season(request, pk):
    season = get_object_or_404(Season, pk=pk)
    forms = SeasonForm(instance=season)
    if request.method == 'POST':
        forms = SeasonForm(request.POST, instance=season)
        if forms.is_valid():
            season = forms.save()
            messages.success(request, f'Season "{season.name}" has been updated.')
            return redirect('season-list')
    return render(request, 'store/create_season.html', {
        'form': forms,
        'is_edit': True,
        'instance': season,
    })


@admin_required
@require_POST
def delete_season(request, pk):
    season = get_object_or_404(Season, pk=pk)
    name = season.name
    season.delete()
    messages.success(request, f'Season "{name}" has been deleted.')
    return redirect('season-list')


class SeasonListView(RoleContextMixin, ListView):
    model = Season
    template_name = 'store/season_list.html'
    context_object_name = 'season'

    def get_queryset(self):
        return Season.objects.all().order_by('-id')


# Drop views
@admin_required
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            drop = forms.save()
            messages.success(request, f'Warehouse drop "{drop.name}" has been created.')
            return redirect('drop-list')
    return render(request, 'store/create_drop.html', {'form': forms, 'is_edit': False})


@admin_required
def edit_drop(request, pk):
    drop = get_object_or_404(Drop, pk=pk)
    forms = DropForm(instance=drop)
    if request.method == 'POST':
        forms = DropForm(request.POST, instance=drop)
        if forms.is_valid():
            drop = forms.save()
            messages.success(request, f'Warehouse drop "{drop.name}" has been updated.')
            return redirect('drop-list')
    return render(request, 'store/create_drop.html', {
        'form': forms,
        'is_edit': True,
        'instance': drop,
    })


@admin_required
@require_POST
def delete_drop(request, pk):
    drop = get_object_or_404(Drop, pk=pk)
    name = drop.name
    drop.delete()
    messages.success(request, f'Warehouse drop "{name}" has been deleted.')
    return redirect('drop-list')


class DropListView(RoleContextMixin, ListView):
    model = Drop
    template_name = 'store/drop_list.html'
    context_object_name = 'drop'

    def get_queryset(self):
        return Drop.objects.all().order_by('-id')


# Product views
@admin_required
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            product = forms.save()
            messages.success(request, f'Product "{product.name}" has been added.')
            return redirect('product-list')
    return render(request, 'store/create_product.html', {'form': forms, 'is_edit': False})


@admin_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    forms = ProductForm(instance=product)
    if request.method == 'POST':
        forms = ProductForm(request.POST, instance=product)
        if forms.is_valid():
            product = forms.save()
            messages.success(request, f'Product "{product.name}" has been updated.')
            return redirect('product-list')
    return render(request, 'store/create_product.html', {
        'form': forms,
        'is_edit': True,
        'instance': product,
    })


@admin_required
@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.success(request, f'Product "{name}" has been deleted.')
    return redirect('product-list')


class ProductListView(RoleContextMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.all().order_by('-id')


# Order views
@admin_required
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            order = Order.objects.create(
                supplier=forms.cleaned_data['supplier'],
                product=forms.cleaned_data['product'],
                design=forms.cleaned_data['design'],
                color=forms.cleaned_data['color'],
                buyer=forms.cleaned_data['buyer'],
                season=forms.cleaned_data['season'],
                drop=forms.cleaned_data['drop'],
                status='pending'
            )
            messages.success(request, f'Order "{order.design}" created with Pending status.')
            return redirect('order-list')
    return render(request, 'store/create_order.html', {'form': forms, 'is_edit': False})


@admin_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    forms = OrderEditForm(instance=order)
    if request.method == 'POST':
        forms = OrderEditForm(request.POST, instance=order)
        if forms.is_valid():
            order = forms.save()
            messages.success(request, f'Order "{order.design}" has been updated.')
            return redirect('order-list')
    return render(request, 'store/create_order.html', {
        'form': forms,
        'is_edit': True,
        'instance': order,
    })


@admin_required
@require_POST
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status', '').strip()
    valid_statuses = dict(Order.STATUS_CHOICE)
    if new_status in valid_statuses:
        order.status = new_status
        order.save(update_fields=['status'])
        messages.success(
            request,
            f'Order "{order.design}" status updated to {valid_statuses[new_status]}.'
        )
    else:
        messages.error(request, 'Invalid order status selected.')
    return redirect('order-list')


@admin_required
@require_POST
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    design = order.design
    order.delete()
    messages.success(request, f'Order "{design}" has been deleted.')
    return redirect('order-list')


class OrderListView(RoleContextMixin, ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_queryset(self):
        qs = Order.objects.select_related(
            'supplier', 'product', 'buyer', 'season', 'drop'
        ).order_by('-id')
        user = self.request.user
        if not is_admin_user(user):
            if user.is_supplier:
                qs = qs.filter(supplier__user=user)
            elif user.is_buyer:
                qs = qs.filter(buyer__user=user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_queryset()
        context['status_choices'] = Order.STATUS_CHOICE
        return context


# Delivery views
@admin_required
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            delivery = forms.save()
            messages.success(request, f'Delivery via "{delivery.courier_name}" has been logged.')
            return redirect('delivery-list')
    return render(request, 'store/create_delivery.html', {'form': forms, 'is_edit': False})


@admin_required
def edit_delivery(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)
    forms = DeliveryForm(instance=delivery)
    if request.method == 'POST':
        forms = DeliveryForm(request.POST, instance=delivery)
        if forms.is_valid():
            delivery = forms.save()
            messages.success(request, f'Delivery via "{delivery.courier_name}" has been updated.')
            return redirect('delivery-list')
    return render(request, 'store/create_delivery.html', {
        'form': forms,
        'is_edit': True,
        'instance': delivery,
    })


@admin_required
@require_POST
def delete_delivery(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)
    courier = delivery.courier_name
    delivery.delete()
    messages.success(request, f'Delivery record ({courier}) has been deleted.')
    return redirect('delivery-list')


class DeliveryListView(RoleContextMixin, ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'

    def get_queryset(self):
        qs = Delivery.objects.select_related(
            'order', 'order__product', 'order__buyer', 'order__supplier'
        ).order_by('-id')
        user = self.request.user
        if not is_admin_user(user):
            if user.is_supplier:
                qs = qs.filter(order__supplier__user=user)
            elif user.is_buyer:
                qs = qs.filter(order__buyer__user=user)
        return qs
