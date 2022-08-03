# Generated by Django 2.2.16 on 2020-12-10 13:12

from django.db import migrations


def set_business_areas(apps, schema_editor):
    Individual = apps.get_model("household", "Individual")
    BusinessArea = apps.get_model("core", "BusinessArea")
    Individual.objects.all().update(business_area=BusinessArea.objects.first())


def revert_setting_business_areas(apps, schema_editor):
    Individual = apps.get_model("household", "Individual")
    Individual.objects.all().update(business_area=None)


class Migration(migrations.Migration):

    dependencies = [
        ("household", "0037_migration"),
    ]

    operations = [
        migrations.RunPython(set_business_areas, revert_setting_business_areas),
    ]
