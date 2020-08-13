# Generated by Django 2.2.8 on 2020-07-23 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targeting', '0008_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='householdselection',
            name='final',
            field=models.BooleanField(
                default=True, help_text='\n            When set to True, this means the household has been selected from\n            the candidate list. Only these households will be sent to\n            CashAssist when a sync is run for the associated target population.\n            '),
        ),
    ]
