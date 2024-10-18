# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Product, Order
from django.core.exceptions import ValidationError
import re

# Seznam zakázaných slov pro validaci uživatelského jména
PROHIBITED_USERNAMES = ['admin', 'administrator', 'superuser', 'staff', 'manager']

# Funkce pro kontrolu sprostých slov
def contains_prohibited_words(value):
    prohibited_words = ['badword1', 'badword2', 'badword3']  # Nahraďte skutečnými slovy
    if any(word in value.lower() for word in prohibited_words):
        raise ValidationError('Uživatelské jméno obsahuje zakázaná slova.')

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.lower() in PROHIBITED_USERNAMES:
            raise forms.ValidationError("Toto uživatelské jméno není povoleno.")
        contains_prohibited_words(username)
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Kontrola opakujících se znaků
        if re.search(r'(.)\1{2,}', password1):
            raise forms.ValidationError("Heslo obsahuje příliš mnoho opakujících se znaků.")

        if password1 != password2:
            raise forms.ValidationError("Hesla se neshodují.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError("Email musí obsahovat znak '@'.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento e-mail je již registrován.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.lower() in PROHIBITED_USERNAMES:
            raise forms.ValidationError("Toto uživatelské jméno není povoleno.")
        contains_prohibited_words(username)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError("Email musí obsahovat znak '@'.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'address', 'avatar', 'role', 'communication_channel']

class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Vyhledat produkty')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image_url', 'category', 'availability', 'author', 'image',
                  'stock']  # Přidáno 'stock'

class OrderCreateForm(forms.ModelForm):
    # Přidáme nová pole pro nepřihlášené uživatele
    first_name = forms.CharField(max_length=50, label='Jméno')
    last_name = forms.CharField(max_length=50, label='Příjmení')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'delivery_method', 'payment_method']
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
