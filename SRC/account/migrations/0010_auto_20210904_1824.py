# Generated by Django 3.2.5 on 2021-09-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_address_is_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.AddField(
            model_name='address',
            name='code',
            field=models.IntegerField(null=True, verbose_name='کد پستی'),
        ),
    ]
