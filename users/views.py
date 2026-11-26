from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, TarindoPasswordChangeForm


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
            forms.add_error(None, 'Invalid username or password. Please check your credentials and try again.')
    context = {'form': forms}
    return render(request, 'users/login.html', context)


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
