# Generated by Django 3.2.9 on 2022-01-22 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_cart_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.store'),
        ),
    ]