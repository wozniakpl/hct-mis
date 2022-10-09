# Generated by Django 2.2.8 on 2020-04-29 08:18

import uuid

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations, models

import model_utils.fields

import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessArea',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('long_name', models.CharField(max_length=255)),
                ('region_code', models.CharField(max_length=8)),
                ('region_name', models.CharField(max_length=8)),
                ('kobo_token', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.CharField(db_index=True, max_length=250, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FlexibleAttributeGroup',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('label', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('required', models.BooleanField(default=False)),
                ('repeatable', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.FlexibleAttributeGroup', verbose_name='Parent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlexibleAttribute',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('STRING', 'String'), ('IMAGE', 'Image'), ('INTEGER', 'Integer'), ('DECIMAL', 'Decimal'), ('SELECT_ONE', 'Select One'), ('SELECT_MANY', 'Select Many'), ('DATETIME', 'Datetime'), ('GEOPOINT', 'Geopoint')], max_length=16)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('required', models.BooleanField(default=False)),
                ('label', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('hint', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('associated_with', models.SmallIntegerField(choices=[(0, 'Household'), (1, 'Individual')])),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flex_attributes', to='core.FlexibleAttributeGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminAreaType',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name')),
                ('display_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Display Name')),
                ('admin_level', models.PositiveSmallIntegerField(verbose_name='Admin Level')),
                ('business_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_area_types', to='core.BusinessArea')),
            ],
            options={
                'verbose_name': 'AdminAreaType type',
                'ordering': ['name'],
                'unique_together': {('business_area', 'admin_level')},
            },
        ),
        migrations.CreateModel(
            name='FlexibleAttributeChoice',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('list_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('label', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('admin', models.CharField(max_length=255)),
                ('flex_attributes', models.ManyToManyField(related_name='choices', to='core.FlexibleAttribute')),
            ],
            options={
                'unique_together': {('list_name', 'name')},
            },
        ),
        migrations.CreateModel(
            name='AdminArea',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('admin_area_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='core.AdminAreaType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.AdminArea', verbose_name='Parent')),
            ],
            options={
                'ordering': ['title'],
                'unique_together': {('title', 'admin_area_type')},
            },
        ),
    ]
