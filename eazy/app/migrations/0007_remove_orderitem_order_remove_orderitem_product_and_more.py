# Generated by Django 4.2.16 on 2024-12-06 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_product_dis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]