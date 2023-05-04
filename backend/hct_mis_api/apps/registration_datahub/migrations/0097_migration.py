# Generated by Django 3.2.18 on 2023-04-04 09:30

from django.db import migrations, models
from django.db.models.functions import Lower


def update_document_type_keys(apps, schema_editor):
    ImportedDocumentType = apps.get_model("registration_datahub", "ImportedDocumentType")
    ImportedDocumentType.objects.all().update(key=Lower("key"))


class Migration(migrations.Migration):

    dependencies = [
        ("registration_datahub", "0096_migration"),
    ]

    operations = [
        migrations.RenameField("ImportedDocumentType", "type", "key"),
        migrations.RunPython(update_document_type_keys, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="importeddocumenttype",
            name="key",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]