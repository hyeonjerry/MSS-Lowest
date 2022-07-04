# Generated by Django 4.0.5 on 2022-07-04 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]