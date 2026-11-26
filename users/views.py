from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from SI.models import Buyer, Supplier
from SI.permissions import admin_required
from .forms import LoginForm, PartnerRegistrationForm, TarindoPasswordChangeForm
from .models import User


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if not request.POST.get('remember_me'):
                    request.session.set_expiry(0)
                return redirect('dashboard')
            pending_user = User.objects.filter(username=username, is_active=False).first()
            if pending_user and pending_user.check_password(password):
                forms.add_error(
                    None,
                    'Your account is pending administrator approval. Please wait until an administrator activates it.'
                )
            else:
                forms.add_error(None, 'Invalid username or password. Please check your credentials and try again.')
    context = {'form': forms}
    return render(request, 'users/login.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = PartnerRegistrationForm()
    submitted = False
    if request.method == 'POST':
        form = PartnerRegistrationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']

            if password != retype_password:
                form.add_error('retype_password', 'Passwords do not match.')
            elif User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
            elif role == 'supplier' and Supplier.objects.filter(name=name).exists():
                form.add_error('name', 'A supplier with this name already exists.')
            elif role == 'buyer' and Buyer.objects.filter(name=name).exists():
                form.add_error('name', 'A buyer with this name already exists.')
            else:
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password=password,
                            is_active=False,
                            is_supplier=(role == 'supplier'),
                            is_buyer=(role == 'buyer'),
                        )
                        if role == 'supplier':
                            Supplier.objects.create(user=user, name=name, address=address)
                        else:
                            Buyer.objects.create(user=user, name=name, address=address)
                    submitted = True
                except IntegrityError:
                    form.add_error(None, 'Could not complete registration. Please check your details and try again.')
    return render(request, 'users/register.html', {'form': form, 'submitted': submitted})


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_page(request):
    password_form = TarindoPasswordChangeForm(request.user)
    if request.method == 'POST':
        password_form = TarindoPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')
    return render(request, 'users/profile.html', {'password_form': password_form})


@admin_required
def pending_approvals_page(request):
    pending_users = (
        User.objects.filter(is_active=False)
        .filter(Q(is_supplier=True) | Q(is_buyer=True))
        .select_related('supplier', 'buyer')
        .order_by('-date_joined')
    )
    items = []
    for u in pending_users:
        profile = getattr(u, 'supplier', None) if u.is_supplier else getattr(u, 'buyer', None)
        items.append({
            'user': u,
            'role': 'Supplier' if u.is_supplier else 'Buyer',
            'company_name': profile.name if profile else u.username,
            'address': profile.address if profile else '—',
        })
    return render(request, 'users/approvals.html', {'pending_items': items})


@admin_required
@require_POST
def approve_account(request, user_id):
    user = get_object_or_404(
        User.objects.filter(is_active=False).filter(Q(is_supplier=True) | Q(is_buyer=True)),
        pk=user_id,
    )
    user.is_active = True
    user.save(update_fields=['is_active'])
    messages.success(request, f'Account "{user.username}" has been approved and activated.')
    return redirect('pending-approvals')


@admin_required
@require_POST
def reject_account(request, user_id):
    user = get_object_or_404(
        User.objects.filter(is_active=False).filter(Q(is_supplier=True) | Q(is_buyer=True)),
        pk=user_id,
    )
    username = user.username
    with transaction.atomic():
        user.delete()
    messages.success(request, f'Pending registration for "{username}" has been rejected and removed.')
    return redirect('pending-approvals')
