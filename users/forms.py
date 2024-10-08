from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Product, Order


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Ujistíme se, že email je povinný

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento e-mail je již registrován.")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Zajištění, že email je povinný

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'address', 'avatar', 'role', 'communication_channel']


class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Vyhledat produkty')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image_url', 'category', 'availability', 'author', 'image']


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'delivery_method', 'payment_method']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vaše adresa'}),
            'delivery_method': forms.RadioSelect(),
            'payment_method': forms.RadioSelect(),
        }
        labels = {
            'address': 'Adresa',
            'delivery_method': 'Způsob dopravy',
            'payment_method': 'Způsob platby',
        }
