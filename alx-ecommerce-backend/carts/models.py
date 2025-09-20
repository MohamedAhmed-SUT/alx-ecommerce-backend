from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    @property
    def total_with_shipping(self):
        shipping = 5  
        return self.total_price() + shipping + self.tax


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    def total_price(self):
        return self.product.price * self.quantity
