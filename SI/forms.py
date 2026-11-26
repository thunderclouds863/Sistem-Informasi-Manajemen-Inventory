from django import forms

from .models import Season, Drop, Product, Order, Delivery


class SupplierForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'name',
        'placeholder': 'e.g. PT Logam Kuningan Jaya',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(max_length=220, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'address',
        'placeholder': 'e.g. Kawasan Industri Tangerang',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'tarindo-input',
        'id': 'email',
        'placeholder': 'supplier@company.co.id',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'username',
        'placeholder': 'e.g. supplier_kuningan',
        'autocomplete': 'off',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'tarindo-input',
        'id': 'password',
        'placeholder': 'Minimum 6 characters',
        'autocomplete': 'new-password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'tarindo-input',
        'id': 'retype_password',
        'placeholder': 'Re-enter password',
        'autocomplete': 'new-password',
        'data-val': 'true',
        'data-val-required': 'Please confirm password',
    }))


class SupplierEditForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'name',
        'placeholder': 'e.g. PT Logam Kuningan Jaya',
    }))
    address = forms.CharField(max_length=220, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'address',
        'placeholder': 'e.g. Kawasan Industri Tangerang',
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'tarindo-input',
        'id': 'email',
        'placeholder': 'supplier@company.co.id',
    }))


class BuyerForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'name',
        'placeholder': 'e.g. Toko Bangunan Sentosa',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(max_length=220, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'address',
        'placeholder': 'e.g. Jl. Raya Jakarta Barat',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'tarindo-input',
        'id': 'email',
        'placeholder': 'purchasing@buyer.co.id',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'username',
        'placeholder': 'e.g. buyer_sentosa',
        'autocomplete': 'off',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'tarindo-input',
        'id': 'password',
        'placeholder': 'Minimum 6 characters',
        'autocomplete': 'new-password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'tarindo-input',
        'id': 'retype_password',
        'placeholder': 'Re-enter password',
        'autocomplete': 'new-password',
        'data-val': 'true',
        'data-val-required': 'Please confirm password',
    }))


class BuyerEditForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'name',
        'placeholder': 'e.g. Toko Bangunan Sentosa',
    }))
    address = forms.CharField(max_length=220, widget=forms.TextInput(attrs={
        'class': 'tarindo-input',
        'id': 'address',
        'placeholder': 'e.g. Jl. Raya Jakarta Barat',
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'tarindo-input',
        'id': 'email',
        'placeholder': 'purchasing@buyer.co.id',
    }))


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'tarindo-input',
                'id': 'name',
                'placeholder': 'e.g. Q3 2026',
            }),
            'description': forms.TextInput(attrs={
                'class': 'tarindo-input',
                'id': 'description',
                'placeholder': 'e.g. Kuartal 3 — Musim Produksi Pipa & Kran',
            })
        }


class DropForm(forms.ModelForm):
    class Meta:
        model = Drop
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'tarindo-input',
                'id': 'name',
                'placeholder': 'e.g. Gudang Finishing Utara',
            })
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sortno']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'tarindo-input',
                'id': 'name',
                'placeholder': 'e.g. Kran Kuningan 1/2"',
            }),
            'sortno': forms.NumberInput(attrs={
                'class': 'tarindo-input',
                'id': 'sortno',
                'placeholder': 'e.g. 250',
                'min': '0',
            })
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'supplier', 'product', 'design', 'color', 'buyer', 'season', 'drop'
        ]

        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'tarindo-select', 'id': 'supplier'
            }),
            'product': forms.Select(attrs={
                'class': 'tarindo-select', 'id': 'product'
            }),
            'design': forms.TextInput(attrs={
                'class': 'tarindo-input',
                'id': 'design',
                'placeholder': 'e.g. D-108',
            }),
            'color': forms.TextInput(attrs={
                'class': 'tarindo-input',
                'id': 'color',
                'placeholder': 'e.g. Gold, Silver, Putih',
            }),
            'buyer': forms.Select(attrs={
                'class': 'tarindo-select', 'id': 'buyer'
            }),
            'season': forms.Select(attrs={
                'class': 'tarindo-select', 'id': 'season'
            }),
            'drop': forms.Select(attrs={
                'class': 'tarindo-select', 'id': 'drop'
            }),
        }


class OrderEditForm(OrderForm):
    class Meta(OrderForm.Meta):
        fields = [
            'supplier', 'product', 'design', 'color',
            'buyer', 'season', 'drop', 'status'
        ]
        widgets = dict(OrderForm.Meta.widgets, **{
            'status': forms.Select(attrs={
                'class': 'tarindo-select', 'id': 'status'
            }),
        })


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['order', 'courier_name']

        widgets = {
            'order': forms.Select(attrs={
                'class': 'tarindo-select', 'id': 'order'
            }),
            'courier_name': forms.TextInput(attrs={
                'class': 'tarindo-input',
                'id': 'courier_name',
                'placeholder': 'e.g. JNE Cargo, Lalamove, Indah Logistik',
            }),
        }
