# Generated by Django 4.2.7 on 2024-01-31 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0023_remove_orders_quantity_orders_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='Quantity',
            new_name='quantity',
        ),
    ]
