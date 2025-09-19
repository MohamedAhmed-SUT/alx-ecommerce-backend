from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    
    brand = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Weight in KG")
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name
