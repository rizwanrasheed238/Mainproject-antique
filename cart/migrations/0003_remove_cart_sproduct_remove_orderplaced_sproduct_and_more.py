# Generated by Django 4.1.1 on 2023-03-10 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cart_sproduct_orderplaced_sproduct_wishlist_sproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='sproduct',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='sproduct',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='sproduct',
        ),
    ]
