# Generated by Django 2.2.8 on 2020-03-12 13:33

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import targeting.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targeting', '0002_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterAttrType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flex_field_types', django.contrib.postgres.fields.jsonb.JSONField()),
                ('core_field_types', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='targetpopulation',
            name='num_individuals_household',
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='_total_family_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='_total_households',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='last_edited_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='status',
            field=models.CharField(choices=[('IN_PROGRESS', 'In Progress'), ('FINALIZED', 'Finalized')], default=targeting.models.TargetStatus('In Progress'), max_length=256),
        ),
        migrations.CreateModel(
            name='TargetRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flex_rules', django.contrib.postgres.fields.jsonb.JSONField()),
                ('core_rules', django.contrib.postgres.fields.jsonb.JSONField()),
                ('target_population', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='target_rules', to='targeting.TargetPopulation')),
            ],
        ),
    ]
