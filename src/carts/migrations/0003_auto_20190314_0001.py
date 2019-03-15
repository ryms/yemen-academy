# Generated by Django 2.1.7 on 2019-03-13 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_timestamp'),
        ('carts', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('count_item', models.IntegerField(default=1)),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
            ],
            options={
                'verbose_name': 'Product in basket',
                'verbose_name_plural': 'Product in basket',
            },
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_items',
            field=models.ManyToManyField(blank=True, to='carts.ProductInCart'),
        ),
    ]
