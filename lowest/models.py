from django.db import models


class Brands(models.Model):
    path = models.CharField(max_length=40, primary_key=True)
    ko_name = models.CharField(max_length=30)
    en_name = models.CharField(max_length=40)
    img = models.CharField(max_length=255)
    created_date = models.DateTimeField()


class History(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    price = models.IntegerField()
    created_date = models.DateTimeField()


class Products(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lowest = models.ForeignKey(
        'History', on_delete=models.CASCADE, related_name='lowest')
    current = models.ForeignKey(
        'History', on_delete=models.CASCADE, related_name='current')
    highest = models.ForeignKey(
        'History', on_delete=models.CASCADE, related_name='highest')
    img = models.CharField(max_length=255)
