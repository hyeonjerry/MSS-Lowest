from django.db import models

from brands.models import Brand


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=250)
    url = models.URLField(max_length=250, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.IntegerField()
    latest_price = models.OneToOneField('ProductHistory',
                                        on_delete=models.SET_NULL,
                                        null=True, blank=True,
                                        related_name='latest')
    lowest_price = models.OneToOneField('ProductHistory',
                                        on_delete=models.SET_NULL,
                                        null=True, blank=True,
                                        related_name='lowest')
    highest_price = models.OneToOneField('ProductHistory',
                                         on_delete=models.SET_NULL,
                                         null=True, blank=True,
                                         related_name='highest')
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
