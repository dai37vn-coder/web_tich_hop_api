# Generated by Django 4.2.7 on 2024-01-31 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0022_alter_orders_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orders',
            name='Quantity',
            field=models.IntegerField(null=True),
        ),
    ]
