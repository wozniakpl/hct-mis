# Generated by Django 2.2.16 on 2021-01-07 11:39

import concurrency.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0019_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='grievanceticket',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
    ]
