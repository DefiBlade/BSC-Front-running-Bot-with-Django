# Generated by Django 3.1.5 on 2021-03-09 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WapsClient', '0007_auto_20210309_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='limitasset',
            old_name='curr_price_for_qnty',
            new_name='curr_price',
        ),
        migrations.RemoveField(
            model_name='limitasset',
            name='curr_price_per_token',
        ),
    ]