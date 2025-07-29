from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
# This code registers the Category and Product models with the Django admin site,
# allowing them to be managed through the admin interface.
