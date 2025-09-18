# carts/admin.py
from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")  # شيلت updated_at لو مش عندك
    search_fields = ("user__username",)
    list_filter = ("created_at",)  # 👈 الفاصلة هنا مهمة جدًا


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
    search_fields = ("product__name",)
