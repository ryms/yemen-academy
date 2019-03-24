# Generated by Django 2.1.7 on 2019-03-24 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
        ('orders', '0005_delete_ordermanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='billing_address', to='addresses.Address', verbose_name='Billing address'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipping_address', to='addresses.Address', verbose_name='Shipping address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'CREATED'), ('paid', 'PAID'), ('shipped', 'SHIPPED'), ('refunder', 'REFUNDER'), ('refunded', 'REFUNDED')], default='created', max_length=120),
        ),
    ]