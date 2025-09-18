from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from carts.models import Cart, CartItem
from products.models import Product
from orders.models import Order, OrderItem
from .forms import ProductForm, OrderForm

# ================= Cart Views =================
@login_required
def cart_page(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product")
    return render(request, "dashboard/cart.html", {
        "cart": cart,
        "items": items,
    })


# ================= Authentication Views =================
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect("dashboard_home")
            else:
                return redirect("shop")
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
            user = form.save()
            messages.success(request, "✅ Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "dashboard/signup.html", {"form": form})


# ================= Shop View for Users =================
@login_required
def shop_view(request):
    products = Product.objects.filter(stock__gt=0)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)

        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} items available for {product.name}.")
            return redirect("shop")

        # 🛒 إضافة المنتج إلى السلة
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, f"🛒 Added {quantity} × {product.name} to your cart")
        return redirect("shop")

    return render(request, "dashboard/shop.html", {"products": products})


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
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from orders.models import Order, OrderItem


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart_page")


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect("cart_page")

    # إنشاء order
    order = Order.objects.create(user=request.user, status="Pending")

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        # خصم من المخزون
        item.product.stock -= item.quantity
        item.product.save()

    # تفريغ الكارت
    cart.items.all().delete()

    return redirect("orders_list")
