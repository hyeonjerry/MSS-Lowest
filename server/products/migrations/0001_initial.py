# Generated by Django 4.1.1 on 2022-09-28 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brands', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField(max_length=250)),
                ('url', models.URLField(max_length=250)),
                ('price', models.IntegerField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brands.brand')),
            ],
        ),
        migrations.CreateModel(
            name='ProductHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='highest_price',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='highest', to='products.producthistory'),
        ),
        migrations.AddField(
            model_name='product',
            name='lowest_price',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lowest', to='products.producthistory'),
        ),
    ]
