from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import csv
import json

# Models & Forms
from orders.models import Order, OrderItem
from carts.models import Cart, CartItem
from products.models import Product, Category
from .forms import ProductForm, OrderForm, CustomUserCreationForm


# ================= Cart Views =================
@login_required
def cart_page(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product")
    return render(request, "dashboard/cart.html", {"cart": cart, "items": items})


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect("cart_page")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart_page")


# ================= Authentication Views =================
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard_home" if user.is_staff else "shop")
    else:
        form = AuthenticationForm()
    return render(request, "dashboard/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account created successfully! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "❌ Please fix the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "dashboard/signup.html", {"form": form})


# ================= Shop Views =================
@login_required
def shop_view(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()

    # filters
    selected_category = request.GET.get("category", "all")
    if selected_category != "all":
        products = products.filter(category__name=selected_category)

    max_price = request.GET.get("max_price")
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            max_price = None

    sort = request.GET.get("sort", "name")
    if sort == "price-low":
        products = products.order_by("price")
    elif sort == "price-high":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")
    else:
        products = products.order_by("name")

    # cart count
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.items.count()

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} items available for {product.name}.")
            return redirect("shop")
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = cart_item.quantity + quantity if not created else quantity
        cart_item.save()
        messages.success(request, f"🛒 Added {quantity} × {product.name} to your cart")
        return redirect("shop")

    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
        "max_price": max_price or 10000,
        "cart_items_count": cart_items_count,
    }
    return render(request, "dashboard/shop.html", context)


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

    orders = Order.objects.all().order_by("-created_at")
    if start_date:
        orders = orders.filter(created_at__date__gte=start_date)

    total_sales = sum(
        sum(item.price * item.quantity for item in order.items.all())
        for order in orders
    )

    context = {
        "users_count": User.objects.count(),
        "products_count": Product.objects.count(),
        "orders_count": orders.count(),
        "total_sales": total_sales,
        "period": period,
        "recent_orders": orders[:5],
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def reports_view(request):
    orders = Order.objects.all().order_by("-created_at")
    total_sales = sum(
        sum(item.price * item.quantity for item in order.items.all())
        for order in orders
    )
    return render(request, "dashboard/reports.html", {"orders": orders, "total_sales": total_sales})


# ================= Products CRUD =================
@login_required
@user_passes_test(lambda u: u.is_staff)
def products_list(request):
    products = Product.objects.all().select_related("category")
    categories = Category.objects.all()

    in_stock = products.filter(stock__gt=10).count()
    low_stock = products.filter(stock__gt=0, stock__lte=10).count()
    out_of_stock = products.filter(stock=0).count()

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "categories": categories,
        "in_stock": in_stock,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
    }
    return render(request, "dashboard/products.html", context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Product added successfully!")
            return redirect("products_list")
    else:
        form = ProductForm()
    return render(request, "dashboard/product_form.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Product updated successfully!")
            return redirect("products_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "dashboard/product_form.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "🗑️ Product deleted successfully!")
    return redirect("products_list")


# ================= Orders =================
@csrf_exempt
@require_POST
def bulk_update_orders(request):
    """Update status for multiple orders"""
    try:
        data = json.loads(request.body)
        ids = data.get("ids", [])
        status = data.get("status", None)

        if not ids or not status:
            return JsonResponse({"error": "Invalid data"}, status=400)

        Order.objects.filter(id__in=ids).update(status=status)
        return JsonResponse({"message": "Orders updated successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def bulk_delete_orders(request):
    """Delete multiple orders"""
    try:
        data = json.loads(request.body)
        ids = data.get("ids", [])

        if not ids:
            return JsonResponse({"error": "No IDs provided"}, status=400)

        Order.objects.filter(id__in=ids).delete()
        return JsonResponse({"message": "Orders deleted successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def orders_list(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by("-created_at")
    else:
        orders = Order.objects.filter(user=request.user).order_by("-created_at")

    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": page_obj,
        "total_orders": orders.count(),
        "completed": orders.filter(status="Completed").count(),
        "processing": orders.filter(status="Processing").count(),
        "pending": orders.filter(status="Pending").count(),
    }
    return render(request, "dashboard/orders.html", context)


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


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect("cart_page")
    order = Order.objects.create(user=request.user, status="Pending")
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order, product=item.product, quantity=item.quantity, price=item.product.price
        )
        item.product.stock -= item.quantity
        item.product.save()
    cart.items.all().delete()
    return redirect("orders_list")


@login_required
@user_passes_test(lambda u: u.is_staff)
def export_orders_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Customer", "Date", "Total", "Status"])

    for order in Order.objects.all():
        writer.writerow([
            order.id,
            order.user.username if order.user else "Guest",
            order.created_at.strftime("%Y-%m-%d"),
            order.total_price() if hasattr(order, "total_price") else sum(i.price * i.quantity for i in order.items.all()),
            order.status,
        ])
    return response


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
        user.is_staff = (role == "admin")
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
