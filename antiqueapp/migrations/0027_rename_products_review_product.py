# Generated by Django 4.1.7 on 2023-05-16 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antiqueapp', '0026_rename_product_review_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='products',
            new_name='product',
        ),
    ]
