# dashboard/forms.py
from django import forms
from products.models import Product
from orders.models import Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "stock", "description", "category"]  

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
