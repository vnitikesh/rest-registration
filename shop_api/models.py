from django.db import models

# Create your models here.

class Shop(models.Model):
    owner = models.ForeignKey('auth.user', related_name = 'shops', on_delete = models.CASCADE)
    shop_name = models.CharField(max_length = 255, blank = True, null = True, default = '')
    created = models.DateTimeField(auto_now_add = True)
    delivery_time = models.CharField(max_length = 70, blank = True, default = '40min')
    discount_coupon = models.CharField(max_length = 128 , blank = True, default = 'new_shop')
    rating = models.FloatField(default= 0)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.shop_name


class Category(models.Model):
    shop = models.ForeignKey(Shop, related_name = 'categories', on_delete = models.CASCADE)
    name = models.CharField(max_length = 255, blank = True, null = True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length = 255, blank = True, db_index = True)
    image = models.ImageField(upload_to = 'products/%Y/%m/%d', blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'categories', null = True, blank = True)
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'shops', null = True, blank = True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
