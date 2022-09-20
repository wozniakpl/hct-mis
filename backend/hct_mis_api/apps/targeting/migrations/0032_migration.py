# Generated by Django 3.2.13 on 2022-08-12 10:45

from collections import defaultdict
from django.db import migrations, models


def remove_duplicate_household_selections(apps, schema_editor):
    HouseholdSelectionModel = apps.get_model("targeting", "HouseholdSelection")

    subquery = (
        HouseholdSelectionModel.objects.filter(
            household=models.OuterRef("household"), target_population=models.OuterRef("target_population")
        )
        .values("household", "target_population")
        .annotate(duplicates_count=models.Count("*"))
    )

    duplicates = (
        HouseholdSelectionModel.objects.annotate(duplicates_count=models.Subquery(subquery.values("duplicates_count")))
        .values("household", "target_population", "duplicates_count", "id")
        .filter(duplicates_count__gt=1, target_population__status="LOCKED")
    )

    groups = defaultdict(list)
    for row in duplicates:
        key = (row["household"], row["target_population"])
        groups[key].append(row["id"])

    for ids in groups.values():
        for id in ids[1:]:
            HouseholdSelectionModel.objects.get(id=id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("household", "0119_migration"),
        ("targeting", "0031_migration"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="householdselection",
            options={"verbose_name": "Household Selection"},
        ),
        migrations.RunPython(remove_duplicate_household_selections),
        migrations.AlterUniqueTogether(
            name="householdselection",
            unique_together={("household", "target_population")},
        ),
    ]
