# Generated by Django 2.2.16 on 2022-01-14 21:07

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


def noop(apps, schema_editor):
    pass


def remove_all_rules(apps, schema_editor):
    TargetPopulation = apps.get_model("targeting", "TargetPopulation")
    Rule = apps.get_model("steficon", "Rule")
    RuleCommit = apps.get_model("steficon", "RuleCommit")
    TargetPopulation._default_manager.update(steficon_rule=None)
    Rule.objects.all().delete()
    RuleCommit.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('steficon', '0006_migration'),
    ]

    operations = [
        migrations.RunPython(remove_all_rules, noop),
    ]
