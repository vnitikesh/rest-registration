# Generated by Django 3.1.4 on 2021-01-20 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('example_api', '0004_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='cart',
        ),
    ]
