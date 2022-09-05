# Generated by Django 3.2.13 on 2022-08-12 18:24

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ("steficon", "0017_migration"),
        ("payment", "0056_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentplan",
            name="steficon_applied_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="paymentplan",
            name="steficon_rule",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="payment_plans",
                to="steficon.rulecommit",
            ),
        ),
        migrations.AddField(
            model_name="paymentplan",
            name="xlsx_file_imported_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="financialserviceprovider",
            name="distribution_limit",
            field=models.DecimalField(
                db_index=True,
                decimal_places=2,
                help_text="The maximum amount of money that can be distributed or unlimited if 0",
                max_digits=12,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
            ),
        ),
        migrations.AlterField(
            model_name="paymentplan",
            name="status",
            field=django_fsm.FSMField(
                choices=[
                    ("OPEN", "Open"),
                    ("LOCKED", "Locked"),
                    ("IN_APPROVAL", "In Approval"),
                    ("IN_AUTHORIZATION", "In Authorization"),
                    ("IN_REVIEW", "In Review"),
                    ("ACCEPTED", "Accepted"),
                    ("STEFICON_WAIT", "Waiting for Rule Engine"),
                    ("STEFICON_RUN", "Rule Engine Running"),
                    ("STEFICON_COMPLETED", "Rule Engine Completed"),
                    ("STEFICON_ERROR", "Rule Engine Errored"),
                    ("XLSX_EXPORTING", "Exporting XLSX file"),
                    ("XLSX_IMPORTING", "Importing XLSX file"),
                ],
                db_index=True,
                default="OPEN",
                max_length=50,
            ),
        ),
    ]
