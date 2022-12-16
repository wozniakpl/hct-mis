# Generated by Django 3.2.15 on 2022-11-14 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("household", "0126_migration"),
        ("grievance", "0052_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketdeletehouseholddetails",
            name="reason_household",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="household.household",
            ),
        ),
    ]

