# Generated by Django 4.1.1 on 2022-10-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0002_brand_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='url',
            field=models.URLField(max_length=250, unique=True),
        ),
    ]
