from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order

# --- User Signup Form ---
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


# --- Product Form ---
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "brand", "weight", "is_active", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"min": "0", "step": "0.01", "class": "form-control"}),
            "stock": forms.NumberInput(attrs={"min": "0", "class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"min": "0", "step": "0.01", "class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }


# --- Order Form ---
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
