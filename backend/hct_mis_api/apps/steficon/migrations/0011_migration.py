# Generated by Django 2.2.16 on 2022-01-23 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('steficon', '0010_migration'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rulecommit',
            unique_together={('rule', 'version')},
        ),
    ]
