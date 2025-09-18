from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView
from django.urls import path
from . import views

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart-detail"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("remove/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
]
