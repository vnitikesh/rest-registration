from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 200, blank = True, null = True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'products')
    name = models.CharField(max_length = 200, null = True, blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    subtotal = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)
    order_items = models.ManyToManyField(Product)
    items_ordered = models.CharField(max_length = 200, blank = True, null = True)


class Checkout(models.Model):
    cart = models.TextField(null = True, blank = True)
    delivery_address = models.TextField()
    item_total_cost = models.DecimalField(max_digits = 10, decimal_places = 2)
    delivery_charge = models.DecimalField(max_digits = 10, decimal_places = 2, default = 42.00)
    total = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.delivery_address
