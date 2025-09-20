from rest_framework import serializers
from carts.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        source="product.price", 
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "price", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price"]

    def get_total_price(self, obj):
        return sum(item.total_price() for item in obj.items.all())
