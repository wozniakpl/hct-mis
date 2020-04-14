# Generated by Django 2.2.8 on 2020-01-30 20:19

import uuid

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('household', '0001_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetPopulation',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, blank=True)),
                ('rules', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='target_populations', to=settings.AUTH_USER_MODEL)),
                ('households', models.ManyToManyField(related_name='target_populations', to='household.Household')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
