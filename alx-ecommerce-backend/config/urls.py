from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="E-Commerce API",
      default_version='v1',
      description="API documentation for E-Commerce Backend",
      contact=openapi.Contact(email="youremail@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', lambda request: redirect('schema-swagger-ui', permanent=False)),

    path('admin/', admin.site.urls),

    # APIs 
    path('api/', include('products.urls')),

    # Users (signup + profile)
    path('api/users/', include('users.urls')),  

    # Authentication JWT
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Orders API
    path('api/', include('orders.urls')),

    # Swagger / Redoc URLs
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("dashboard/", include("dashboard.urls")),

]
