# Generated by Django 2.2.16 on 2021-01-21 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminarea',
            old_name='admin_area_type',
            new_name='admin_area_level',
        ),
    ]
