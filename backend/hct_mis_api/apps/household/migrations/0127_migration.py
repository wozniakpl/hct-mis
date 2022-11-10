# Generated by Django 3.2.15 on 2022-11-04 14:17

from django.db import migrations, models, transaction
from hct_mis_api.apps.utils.phone import calculate_phone_numbers_validity


@transaction.atomic
def update_each_phone_numbers_validity(apps, schema_editor):
    Individual = apps.get_model("household", "Individual")
    individuals = []
    for individual in Individual.objects.only(
        "phone_no", "phone_no_alternative", "phone_no_valid", "phone_no_alternative_valid"
    ).iterator():
        individual = calculate_phone_numbers_validity(individual)
        individuals.append(individual)
        if len(individuals) == 1000:
            Individual.objects.bulk_update(individuals, ["phone_no_valid", "phone_no_alternative_valid"])
            individuals = []
    if individuals:
        Individual.objects.bulk_update(individuals, ["phone_no_valid", "phone_no_alternative_valid"])


class Migration(migrations.Migration):

    dependencies = [
        ("household", "0126_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="individual",
            name="phone_no_alternative_valid",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name="individual",
            name="phone_no_valid",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.RunPython(update_each_phone_numbers_validity, migrations.RunPython.noop),
    ]
