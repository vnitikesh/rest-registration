# Generated by Django 3.1.4 on 2021-01-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example_api', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items_ordered',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]