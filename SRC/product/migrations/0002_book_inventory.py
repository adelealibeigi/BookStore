# Generated by Django 3.2.5 on 2021-08-20 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='inventory',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
