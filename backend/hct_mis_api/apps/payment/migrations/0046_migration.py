# Generated by Django 3.2.13 on 2022-07-05 07:17

import django.contrib.postgres.fields
from django.db import migrations, models


def get_cash_plan_payment_verification_model(apps):
    return apps.get_model("payment", "CashPlanPaymentVerification")


class Migrator:
    uuids = []

    @staticmethod
    def save_current_uuids(apps, schema_editor):
        for cppv in get_cash_plan_payment_verification_model(apps).objects.all():
            if cppv.rapid_pro_flow_start_uuid:
                Migrator.uuids.append({"cppv": cppv.pk, "uuid": cppv.rapid_pro_flow_start_uuid})

    @staticmethod
    def apply_saved_uuids(apps, schema_editor):
        for uuid in Migrator.uuids:
            cppv = get_cash_plan_payment_verification_model(apps).objects.get(pk=uuid["cppv"])
            cppv.rapid_pro_flow_start_uuids = [uuid["uuid"]]
            cppv.save()


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0045_migration"),
    ]

    operations = [
        migrations.RunPython(Migrator.save_current_uuids, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="cashplanpaymentverification",
            name="rapid_pro_flow_start_uuid",
        ),
        migrations.AddField(
            model_name="cashplanpaymentverification",
            name="rapid_pro_flow_start_uuids",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=255), default=list, size=None
            ),
            preserve_default=False,
        ),
        migrations.RunPython(Migrator.apply_saved_uuids, reverse_code=migrations.RunPython.noop),
    ]
