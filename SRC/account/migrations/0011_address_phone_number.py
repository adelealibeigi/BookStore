# Generated by Django 3.2.5 on 2021-09-04 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20210904_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=models.IntegerField(null=True, verbose_name='شماره تماس'),
        ),
    ]