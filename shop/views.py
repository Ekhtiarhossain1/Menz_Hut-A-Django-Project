from .models import Customer
from django.contrib import messages
import hashlib
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Customer.objects.get(username=username)
            if user.check_password(password):
                request.session['customer_id'] = user.id
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = Customer(username=username, address=address)
            user.set_password(password)
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    request.session.pop('customer_id', None)
    return redirect('home')
def find_store(request):
    return render(request, 'find_store.html')
from django.http import JsonResponse
from django.views.decorators.http import require_POST
@require_POST
def ajax_add_to_cart(request):
    product_id = request.POST.get('product_id')
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.add(product, size, quantity)
    return JsonResponse({'success': True, 'cart_count': len(cart)})

def ajax_cart_count(request):
    cart = Cart(request)
    return JsonResponse({'cart_count': len(cart)})
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Category, Product
from .cart import Cart


def home(request):
    SUMMER = Product.objects.filter(category__name='SUMMER')[:6]
    CASUAL_SHIRT = Product.objects.filter(category__name='CASUAL SHIRT')[:6]
    FORMAL_SHIRT = Product.objects.filter(category__name='FORMAL SHIRT')[:6]
    T_SHIRT = Product.objects.filter(category__name='T-SHIRT')[:6]
    KORTI = Product.objects.filter(category__name='KORTI')[:6]
    PANJABI = Product.objects.filter(category__name='PANJABI')[:6]
    PANT = Product.objects.filter(category__name='PANT')[:6]  
    hot_products = Product.objects.filter(is_hot=True)[:5] 
    return render(request, 'index.html', {'SUMMER': SUMMER,'CASUAL_SHIRT': CASUAL_SHIRT, 
                                          'FORMAL_SHIRT': FORMAL_SHIRT, 'T_SHIRT':T_SHIRT, 
                                          'KORTI':KORTI, 'PANJABI':PANJABI ,'PANT': PANT, 
                                          'hot_products': hot_products,
                                          })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))
        action = request.POST.get('action')
        cart = Cart(request)
        if action == 'add_to_cart':
            cart.add(product, size, quantity)
            return redirect('product_detail', product_id=product.id)
        elif action == 'order_now':
            cart.clear()
            cart.add(product, size, quantity)
            # Here you would create an order, for now just redirect to cart
            return redirect('cart_detail')
    return render(request, 'product_detail.html', {'product': product})
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(product, size, quantity)
    return redirect('cart_detail')

def cart_remove(request, product_id, size):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.remove(product, size)
    return redirect('cart_detail')

def cart_update(request, product_id, size):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(product, size, quantity, update_quantity=True)
    return redirect('cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

def place_order(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    cart = Cart(request)
    # Here you would create an order from cart items for the logged-in customer
    cart.clear()
    return render(request, 'order_success.html')


def category_view(request, category_name):
    if category_name.upper() == 'SALE':
        products = Product.objects.filter(is_hot=True)
        category = {'name': 'SALE'}
    else:
        category = get_object_or_404(Category, name__iexact=category_name)
        products = Product.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'current_category': category_name,
    })
