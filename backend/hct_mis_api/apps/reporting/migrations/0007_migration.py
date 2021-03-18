# Generated by Django 2.2.16 on 2021-03-15 14:57

from django.db import migrations, models
import hct_mis_api.apps.account.models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0006_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardreport',
            name='report_type',
            field=hct_mis_api.apps.account.models.ChoiceArrayField(base_field=models.CharField(choices=[('TOTAL_TRANSFERRED_BY_COUNTRY', 'Total transferred by country'), ('TOTAL_TRANSFERRED_BY_ADMIN_AREA', 'Total transferred by admin area'), ('BENEFICIARIES_REACHED', 'Beneficiaries reached'), ('INDIVIDUALS_REACHED', 'Individuals reached drilldown'), ('VOLUME_BY_DELIVERY_MECHANISM', 'Volume by delivery mechanism'), ('GRIEVANCES_AND_FEEDBACK', 'Grievances and Feedback'), ('PROGRAMS', 'Programmes'), ('PAYMENT_VERIFICATION', 'Payment verification')], max_length=255), size=None),
        ),
    ]
