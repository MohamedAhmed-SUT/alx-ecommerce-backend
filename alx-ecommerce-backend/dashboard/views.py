from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

from products.models import Product
from orders.models import Order
from .forms import ProductForm, OrderForm


# ================= Authentication Views =================
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard_home")
    else:
        form = AuthenticationForm()
    return render(request, "dashboard/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "dashboard/signup.html", {"form": form})


# ================= Admin Dashboard =================
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
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

    total_sales = sum(sum(item.price * item.quantity for item in order.items.all()) for order in orders)

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
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, "🛒 Order created successfully!")
            return redirect("orders_list")
    else:
        form = OrderForm()
    return render(request, "dashboard/order_form.html", {"form": form})


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


# ================= Users Management (Admin Only) =================
@login_required
@user_passes_test(lambda u: u.is_staff)
def users_list(request):
    users = User.objects.all()
    return render(request, "dashboard/users.html", {"users": users})


@login_required
@user_passes_test(lambda u: u.is_staff)
def user_update_role(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        role = request.POST.get("role")
        user.is_staff = True if role == "admin" else False
        user.save()
        messages.success(request, f"✅ Role for {user.username} updated successfully!")
        return redirect("users_list")
    return render(request, "dashboard/user_role_form.html", {"user": user})


@login_required
@user_passes_test(lambda u: u.is_staff)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "🗑️ User deleted successfully!")
        return redirect("users_list")
    return render(request, "dashboard/user_confirm_delete.html", {"user": user})
