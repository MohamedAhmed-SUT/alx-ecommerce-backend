# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.timezone import now, timedelta

from products.models import Product
from orders.models import Order
from .forms import ProductForm, OrderForm


# ================= Admin Dashboard =================
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """عرض إحصائيات عامة عن النظام (Users, Products, Orders, Sales)"""
    period = request.GET.get("period", "all")

    today = now().date()
    start_date = None
    if period == "day":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=7)
    elif period == "month":
        start_date = today.replace(day=1)

    orders = Order.objects.all()
    if start_date:
        orders = orders.filter(created_at__date__gte=start_date)

    users_count = User.objects.count()
    products_count = Product.objects.count()
    orders_count = orders.count()

    total_sales = 0
    for order in orders:
        total_sales += sum(item.price * item.quantity for item in order.items.all())

    context = {
        "users_count": users_count,
        "products_count": products_count,
        "orders_count": orders_count,
        "total_sales": total_sales,
        "period": period,
    }
    return render(request, "dashboard/admin_dashboard.html", context)


# ================= Products CRUD =================
@login_required
def products_list(request):
    products = Product.objects.all()
    return render(request, "dashboard/products.html", {"products": products})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Product added successfully!")
            return redirect("products_list")
    else:
        form = ProductForm()
    return render(request, "dashboard/product_form.html", {"form": form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Product updated successfully!")
            return redirect("products_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "dashboard/product_form.html", {"form": form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "🗑️ Product deleted successfully!")
    return redirect("products_list")


# ================= Orders =================
@login_required
def orders_list(request):
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, "dashboard/orders.html", {"orders": orders})


@login_required
@user_passes_test(lambda u: u.is_staff)
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Order updated successfully!")
            return redirect("orders_list")
    else:
        form = OrderForm(instance=order)
    return render(request, "dashboard/order_form.html", {"form": form})
