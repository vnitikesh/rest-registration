# Generated by Django 3.1.4 on 2021-01-20 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example_api', '0005_remove_checkout_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='cart',
            field=models.TextField(blank=True, null=True),
        ),
    ]
