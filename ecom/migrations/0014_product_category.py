# Generated by Django 4.2.7 on 2023-11-21 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0013_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='product', to='ecom.category'),
        ),
    ]
