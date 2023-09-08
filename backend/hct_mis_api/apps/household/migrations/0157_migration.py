# Generated by Django 3.2.19 on 2023-07-06 13:12

from django.db import migrations, models
import django.db.models.deletion
from django.db.models import OuterRef


def populate_program_in_documents(apps, schema_editor):
    Document = apps.get_model("household", "Document")
    Individual = apps.get_model("household", "Individual")

    Document.objects.all().update(
        program_id=Individual.objects.filter(id=OuterRef("individual_id")).values("program_id")[:1]
    )


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0038_migration'),
        ('household', '0156_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='program.program'),
        ),
        migrations.RunPython(populate_program_in_documents, migrations.RunPython.noop),
        migrations.RemoveConstraint(
            model_name='document',
            name='unique_for_individual_if_not_removed_and_valid',
        ),
        migrations.RemoveConstraint(
            model_name='document',
            name='unique_if_not_removed_and_valid',
        ),
        migrations.AddConstraint(
            model_name='document',
            constraint=models.UniqueConstraint(condition=models.Q(models.Q(('is_removed', False), ('status', 'VALID'), django.db.models.expressions.Func(django.db.models.expressions.F('type_id'), django.db.models.expressions.Value(True), function='check_unique_document_for_individual', output_field=models.BooleanField()))), fields=('type', 'country', 'program'), name='unique_for_individual_if_not_removed_and_valid'),
        ),
        migrations.AddConstraint(
            model_name='document',
            constraint=models.UniqueConstraint(condition=models.Q(models.Q(('is_removed', False), ('status', 'VALID'), django.db.models.expressions.Func(django.db.models.expressions.F('type_id'), django.db.models.expressions.Value(False), function='check_unique_document_for_individual', output_field=models.BooleanField()))), fields=('document_number', 'type', 'country', 'program'), name='unique_if_not_removed_and_valid'),
        ),
    ]
