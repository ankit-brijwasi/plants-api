# Generated by Django 3.1.4 on 2020-12-27 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201228_0050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='Carted',
            new_name='ordered',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='Carted_on',
            new_name='ordered_on',
        ),
    ]
