# Generated by Django 4.1.7 on 2023-05-16 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antiqueapp', '0023_alter_reviewrating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='rating',
            field=models.FloatField(),
        ),
    ]