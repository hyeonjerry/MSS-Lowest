from django.db import models

from brands.models import Brand


class Product(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='brand_product')
    retail_price = models.IntegerField()
    last_price = models.ForeignKey(
        'ProductHistory', on_delete=models.CASCADE, related_name='last_product', null=True, blank=True)
    lowest_price = models.ForeignKey(
        'ProductHistory', on_delete=models.CASCADE, related_name='lowest_product', null=True, blank=True)
    highest_price = models.ForeignKey(
        'ProductHistory', on_delete=models.CASCADE, related_name='highest_product', null=True, blank=True)
    image = models.URLField()
    url = models.URLField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"


class ProductHistory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='producthistory')
    price = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.created_date})"
