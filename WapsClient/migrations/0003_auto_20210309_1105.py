# Generated by Django 3.1.5 on 2021-03-09 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WapsClient', '0002_auto_20210309_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='curr_price',
        ),
        migrations.AddField(
            model_name='limitasset',
            name='curr_price',
            field=models.FloatField(null=True),
        ),
    ]