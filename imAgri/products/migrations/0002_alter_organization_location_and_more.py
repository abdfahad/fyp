# Generated by Django 5.0.4 on 2024-05-07 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='location',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='organization',
            name='password',
            field=models.CharField(max_length=50),
        ),
    ]
