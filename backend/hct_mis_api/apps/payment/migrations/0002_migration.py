# Generated by Django 2.2.8 on 2020-01-31 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymententitlement',
            name='entitlement_card_issue_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
