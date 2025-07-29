from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home(request):
    casual_shirts = Product.objects.filter(category__name='Shirts')[:6]
    pants = Product.objects.filter(category__name='Pants')[:6]  
    hot_products = Product.objects.filter(is_hot=True)[:5] 
    return render(request, 'index.html', {'casual_shirts': casual_shirts, 'pants': pants, 'hot_products': hot_products,})

def about(request):
    return render(request, 'about.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})
