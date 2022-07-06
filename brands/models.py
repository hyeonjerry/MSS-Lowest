from django.db import models


class Brand(models.Model):
    ko_name = models.CharField(max_length=35)
    en_name = models.CharField(max_length=50)
    suffix = models.CharField(
        max_length=50, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return f"{self.ko_name}({self.en_name})"
