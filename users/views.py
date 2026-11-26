from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm


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
