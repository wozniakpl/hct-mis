# Generated by Django 2.2.8 on 2020-04-21 12:34

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0014_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='admin1',
        ),
        migrations.RemoveField(
            model_name='household',
            name='admin2',
        ),
        migrations.RemoveField(
            model_name='household',
            name='household_ca_id',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='individual_ca_id',
        ),
        migrations.AddField(
            model_name='household',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='household',
            name='country_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]
