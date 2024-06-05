# Generated by Django 3.2.25 on 2024-06-04 23:24

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0179_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='registration_id',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Beneficiary Program Registration Id'),
        ),
    ]
