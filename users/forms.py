from django import forms
from django.contrib.auth.forms import PasswordChangeForm


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


class TarindoPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'tarindo-input',
            'id': 'old_password',
            'placeholder': 'Enter current password',
            'autocomplete': 'current-password',
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'tarindo-input',
            'id': 'new_password1',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'tarindo-input',
            'id': 'new_password2',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
        })
