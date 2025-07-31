from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('store/', views.store, name='store'),
    path('find_store/', views.find_store, name='find_store'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_view, name='category'),
]