# Generated by Django 4.1.1 on 2023-03-26 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_alter_seller_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller_product',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]