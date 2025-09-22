# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name="dashboard_home"),
    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('dashboard/reports/', views.reports_view, name='reports_view'),
    # Products CRUD
    path('products/', views.products_list, name="products_list"),
    path('products/add/', views.product_create, name="product_create"),
    path('products/<int:pk>/edit/', views.product_update, name="product_update"),
    path('products/<int:pk>/delete/', views.product_delete, name="product_delete"),

    # Orders
    path('orders/', views.orders_list, name="orders_list"),
    path('orders/create/', views.order_create, name="order_create"),
    path('orders/<int:pk>/update/', views.order_update, name="order_update"),
    path("orders/export/", views.export_orders_csv, name="export_orders_csv"),
    path("bulk/update/", views.bulk_update_orders, name="bulk_update_orders"),
    path("bulk/delete/", views.bulk_delete_orders, name="bulk_delete_orders"),

    # Users Management
    path('users/', views.users_list, name="users_list"),
    path('users/<int:pk>/role/', views.user_update_role, name="user_update_role"),
    path('users/<int:pk>/delete/', views.user_delete, name="user_delete"),
    # Auth
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),

    path('shop/', views.shop_view, name="shop"),
    path("cart/", views.cart_page, name="cart-page"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("cart/", views.cart_page, name="cart_page"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path('cart/clear/', views.clear_cart, name='clear_cart')
    
]
