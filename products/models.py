from django.db import models

from brands.models import Brand


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True, related_name='parent_category')
    name = models.CharField(max_length=25, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='brand_product')
    requested_price = models.IntegerField()
    last_price = models.ForeignKey(
        'ProductHistory', on_delete=models.CASCADE, related_name='last_product')
    lowest_price = models.ForeignKey(
        'ProductHistory', on_delete=models.CASCADE, related_name='lowest_product')
    highest_price = models.ForeignKey(
        'ProductHistory', on_delete=models.CASCADE, related_name='highest_product')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_product')
    thumbnail = models.URLField()
    url = models.URLField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"


class ProductHistory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_producthistory')
    price = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.created_date})"
