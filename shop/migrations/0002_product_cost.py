# Generated by Django 3.2.9 on 2022-01-10 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
