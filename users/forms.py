from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)


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


class PartnerRegistrationForm(forms.Form):
    ROLE_CHOICES = (
        ('buyer', 'Buyer (Hardware Store / Distributor)'),
        ('supplier', 'Supplier (Material / Casting Vendor)'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'tarindo-select',
        'id': 'reg-role',
    }))
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'reg-name',
        'placeholder': 'Company or store name',
    }))
    address = forms.CharField(max_length=220, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'reg-address',
        'placeholder': 'City or full business address',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'tarindo-input',
        'id': 'reg-email',
        'placeholder': 'you@company.co.id',
        'autocomplete': 'email',
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'reg-username',
        'placeholder': 'Choose a username',
        'autocomplete': 'username',
    }))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'tarindo-input',
        'id': 'reg-password',
        'placeholder': 'Minimum 6 characters',
        'autocomplete': 'new-password',
    }))
    retype_password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'tarindo-input',
        'id': 'reg-retype-password',
        'placeholder': 'Confirm your password',
        'autocomplete': 'new-password',
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


class TarindoPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'tarindo-input',
            'id': 'reset-email',
            'placeholder': 'Enter your registered email address',
            'autocomplete': 'email',
        }),
    )


class TarindoSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'tarindo-input',
            'id': 'reset-new-password1',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'tarindo-input',
            'id': 'reset-new-password2',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
        })
