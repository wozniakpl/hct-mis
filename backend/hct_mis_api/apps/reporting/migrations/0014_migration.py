# Generated by Django 3.2.13 on 2022-06-28 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0013_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='admin_area_new',
            new_name='admin_area',
        ),
    ]
