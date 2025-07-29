from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='products/')
    is_hot = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    

    @property
    def final_price(self):
        return round(self.base_price * (1 - self.discount_percentage / 100), 2)

    def __str__(self):
        return self.name
