from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, CheckoutView
from django.urls import path
router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('', include(router.urls)),
    
]
