from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import  Menu, Category, Item, Customer, Order, Order_Item, Sale

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email address'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your Password'})
    )

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'})
    )

class Menus(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('name', 'description',)

        widgets = {
            'name': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
            'class': 'form-control'
            }),
        }

class Categories(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description',)

        widgets = {
            'name': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
            'class': 'form-control'
            }),
        }

class Customers(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'address', 'phone_number', 'email')

        widgets = {
            'name': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
            'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
            'class': 'form-control'
            }),
        }

class Items(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'category', 'description', 'price', 'image',)

        widgets = {
            'name': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'category': forms.Select(attrs={
            'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
            'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
        }

class Orders(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name', 'table_number',)

        widgets = {
            'customer_name': forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Customer Name'
            }),
            'table_number': forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'Table Number'
            }),
        }

class DisabledOrders(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name', 'table_number',)

        widgets = {
            'customer_name': forms.TextInput(attrs={
            'class': 'form-control', 'disabled': True
            }),
            'table_number': forms.NumberInput(attrs={
            'class': 'form-control', 'disabled': True
            }),
        }

class Order_Items(forms.ModelForm):
    class Meta:
        model = Order_Item
        fields = ('order', 'item', 'quantity',)

class Sales(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('order', 'total_amount',)
        labels = {
            'total_amount': 'Total Payment',
        }