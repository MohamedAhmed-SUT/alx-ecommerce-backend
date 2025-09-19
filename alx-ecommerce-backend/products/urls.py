from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)   
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("ajax/add-category/", views.ajax_add_category, name="ajax_add_category"),
]
