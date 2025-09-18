from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        """Return total price for all items in this order."""
        return sum(item.total_price() for item in self.items.all())
    @property
    def total_amount(self):
        return sum(item.price * item.quantity for item in self.items.all())
    @property
    def status_color(self):
        """Map status to Bootstrap badge colors."""
        return {
            'Pending': 'warning',
            'Processing': 'info',
            'Completed': 'success',
            'Cancelled': 'danger'
        }.get(self.status, 'secondary')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        """Return total price for this item."""
        return self.price * self.quantity
