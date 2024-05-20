# Generated by Django 5.0.4 on 2024-05-08 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_products_company_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='company_id',
        ),
        migrations.AddField(
            model_name='products',
            name='org_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.organization'),
            preserve_default=False,
        ),
    ]
