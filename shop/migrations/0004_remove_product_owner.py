# Generated by Django 3.2.9 on 2021-12-29 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20211229_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='owner',
        ),
    ]
