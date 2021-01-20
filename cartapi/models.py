from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 200, null = True, blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.name
