# Generated by Django 3.2.9 on 2022-01-13 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_store_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='image',
            field=models.FileField(default=0, upload_to=''),
        ),
    ]
