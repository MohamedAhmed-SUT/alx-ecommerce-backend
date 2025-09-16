from django.urls import path
from . import views

urlpatterns = [
    # Dashboard 
    path('', views.admin_dashboard, name="dashboard_home"),
    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),  # 👈 هنا

    # Products CRUD
    path('products/', views.products_list, name="products_list"),
    path('products/add/', views.product_create, name="product_create"),
    path('products/<int:pk>/edit/', views.product_update, name="product_update"),
    path('products/<int:pk>/delete/', views.product_delete, name="product_delete"),

    # Orders
    path('orders/', views.orders_list, name="orders_list"),
    path('orders/<int:pk>/update/', views.order_update, name="order_update"),
]
