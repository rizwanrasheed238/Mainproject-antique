# Generated by Django 4.1.1 on 2023-02-28 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antiqueapp', '0002_account_approved_staff_account_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_seller',
        ),
    ]