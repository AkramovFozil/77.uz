# Generated by Django 5.1.5 on 2025-01-23 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_extra_product_remove_image_created_at_and_more'),
        ('common', '0003_remove_address_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='validate_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='common.address'),
        ),
    ]
