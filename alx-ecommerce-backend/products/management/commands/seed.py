from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = "Seed the database with initial categories and products"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        electronics, _ = Category.objects.get_or_create(
            name="Electronics",
            defaults={"description": "Electronic devices and accessories"}
        )

        clothes, _ = Category.objects.get_or_create(
            name="Clothes",
            defaults={"description": "Clothing and apparel"}
        )

        books, _ = Category.objects.get_or_create(
            name="Books",
            defaults={"description": "Books and magazines"}
        )

        Product.objects.get_or_create(
            name="Gaming Laptop",
            defaults={
                "description": "High-performance laptop for gaming",
                "price": 1599.99,
                "stock": 5,
                "category": electronics
            }
        )

        Product.objects.get_or_create(
            name="Wireless Headphones",
            defaults={
                "description": "Noise-cancelling over-ear headphones",
                "price": 199.99,
                "stock": 20,
                "category": electronics
            }
        )

        Product.objects.get_or_create(
            name="Men's T-Shirt",
            defaults={
                "description": "Comfortable cotton t-shirt",
                "price": 19.99,
                "stock": 50,
                "category": clothes
            }
        )

        Product.objects.get_or_create(
            name="Django for Beginners",
            defaults={
                "description": "Practical guide to Django development",
                "price": 29.99,
                "stock": 15,
                "category": books
            }
        )

        self.stdout.write(self.style.SUCCESS("Seeding finished."))
