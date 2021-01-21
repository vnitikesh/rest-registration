from django.db import models
from shop_api.models import Shop
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'categories')
    name = models.CharField(max_length = 200, blank = True, null = True)

    def __str__(self):
        return self.name


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'shop_product')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'products')
    name = models.CharField(max_length = 200, null = True, blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.name




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'cart', null = True, blank = True)
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'shop_cart', null = True, blank = True)
    subtotal = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)
    order_items = models.ManyToManyField(Product)
    items_ordered = models.CharField(max_length = 200, blank = True, null = True)
    quantities = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.user.username



class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'checkout_user', null = True, blank = True)
    cart = models.TextField(null = True, blank = True)
    delivery_address = models.TextField(null = True, blank = True)
    item_total_cost = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    delivery_charge = models.DecimalField(max_digits = 10, decimal_places = 2, default = 42.00, null = True, blank = True)
    total = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)

    def __str__(self):
        return self.delivery_address
