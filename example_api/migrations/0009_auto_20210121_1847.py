# Generated by Django 3.1.4 on 2021-01-21 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop_api', '0004_auto_20210121_1246'),
        ('example_api', '0008_product_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantities',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='shop',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_cart', to='shop_api.shop'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
    ]
