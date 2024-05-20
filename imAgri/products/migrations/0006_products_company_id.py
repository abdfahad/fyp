# Generated by Django 5.0.4 on 2024-05-08 08:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_products_product_alter_products_product_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='company_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.organization'),
            preserve_default=False,
        ),
    ]