# Generated by Django 3.2.5 on 2021-08-19 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_address_is_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='آدرس اصلی'),
        ),
    ]
