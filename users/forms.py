from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'login-username',
        'placeholder': 'Enter your username',
        'autocomplete': 'username',
        'autofocus': 'autofocus',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'tarindo-input',
        'id': 'login-password',
        'placeholder': 'Enter your password',
        'autocomplete': 'current-password',
    }))
