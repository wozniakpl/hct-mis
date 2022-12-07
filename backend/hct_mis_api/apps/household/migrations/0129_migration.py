# Generated by Django 3.2.15 on 2022-11-08 16:30
from functools import lru_cache

from django.db import migrations, models
import django.db.models.deletion

from hct_mis_api.apps.account.models import Partner


@lru_cache(maxsize=None)
def get_partner(model, partner_name: str) -> Partner:
    return model.objects.get(name=partner_name)


@lru_cache(maxsize=None)
def get_country(model, country_id):
    return model.objects.get(id=country_id)


def populate_partner_and_country(apps, schema_editor):
    IndividualIdentity = apps.get_model("household", "IndividualIdentity")
    Partner = apps.get_model("account", "Partner")
    Country = apps.get_model("geo", "Country")

    for identity in IndividualIdentity.objects.all():
        identity.partner = get_partner(Partner, identity.agency.type)
        identity.country = get_country(Country, identity.agency.country_id)
        identity.save(update_fields=("partner", "country"))


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0043_migration"),
        ("geo", "0007_migration"),
        ("household", "0128_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="individualidentity",
            name="country",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="geo.country"),
        ),
        migrations.AddField(
            model_name="individualidentity",
            name="partner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="individual_identities",
                to="account.partner",
            ),
        ),
        migrations.RunPython(populate_partner_and_country, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="individualidentity",
            name="agency",
        ),
        migrations.DeleteModel(
            name="Agency",
        ),
    ]
