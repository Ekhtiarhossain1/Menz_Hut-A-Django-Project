from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home(request):
    SUMMER = Product.objects.filter(category__name='SUMMER')[:6]
    CASUAL_SHIRT = Product.objects.filter(category__name='CASUAL SHIRT')[:6]
    FORMAL_SHIRT = Product.objects.filter(category__name='FORMAL SHIRT')[:6]
    T_SHIRT = Product.objects.filter(category__name='T-SHIRT')[:6]
    KORTI = Product.objects.filter(category__name='KORTI')[:6]
    PANJABI = Product.objects.filter(category__name='PANJABI')[:6]
    PANT = Product.objects.filter(category__name='PANT')[:6]  
    hot_products = Product.objects.filter(is_hot=True)[:5] 
    return render(request, 'index.html', {'SUMMER': SUMMER,'casual_shirts': CASUAL_SHIRT, 
                                          'FORMAL_SHIRT': FORMAL_SHIRT, 'T_SHIRT':T_SHIRT, 
                                          'KORTI':KORTI, 'PANJABI':PANJABI ,'pants': PANT, 
                                          'hot_products': hot_products,
                                          })

def about(request):
    return render(request, 'about.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def category_view(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})
