# Generated by Django 2.2.16 on 2021-05-04 11:57

from django.db import migrations


def cast_flex_field_values(apps, schema_editor):
    pass


def empty_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("registration_datahub", "0036_migration"),
    ]

    operations = [
        migrations.RunPython(cast_flex_field_values, empty_reverse),
    ]
