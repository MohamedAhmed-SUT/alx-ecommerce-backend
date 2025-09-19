from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  
            return True
        return request.user and request.user.is_staff

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_fields = ['category', 'price']
    ordering_fields = ['price', 'stock']
    search_fields = ['name', 'description']
    permission_classes = [IsAdminOrReadOnly]  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Category

@login_required
@csrf_exempt
def ajax_add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            category, created = Category.objects.get_or_create(name=name)
            return JsonResponse({"id": category.id, "name": category.name})
    return JsonResponse({"error": "Invalid request"}, status=400)
