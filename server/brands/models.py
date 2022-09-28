from django.db import models


class Brand(models.Model):
    ko_name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=100)
    url = models.URLField(max_length=250)
