# Generated by Django 3.2.5 on 2021-08-19 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='username',
            new_name='user',
        ),
    ]
