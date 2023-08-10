# Generated by Django 3.2.20 on 2023-08-04 11:18

import concurrency.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0106_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashplan',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
        migrations.AddField(
            model_name='paymentplan',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
    ]
