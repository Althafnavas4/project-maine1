# Generated by Django 5.1.5 on 2025-01-18 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_buy_size_cart_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(related_name='Sizes', to='app.size'),
        ),
    ]
