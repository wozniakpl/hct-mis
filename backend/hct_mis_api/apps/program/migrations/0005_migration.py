# Generated by Django 2.2.8 on 2020-05-22 11:45

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_migration'),
        ('program', '0004_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashPlan',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ca_id', models.CharField(max_length=255)),
                ('ca_hash_id', models.UUIDField(unique=True)),
                ('status', models.CharField(choices=[('Distribution Completed', 'Distribution Completed'), ('Distribution Completed with Errors', 'Distribution Completed with Errors'), ('Transaction Completed', 'Transaction Completed'), ('Transaction Completed with Errors', 'Transaction Completed with Errors')], max_length=255)),
                ('status_date', models.DateTimeField()),
                ('name', models.CharField(max_length=255)),
                ('distribution_level', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('dispersion_date', models.DateTimeField()),
                ('coverage_duration', models.PositiveIntegerField()),
                ('coverage_unit', models.CharField(max_length=255)),
                ('comments', models.CharField(max_length=255)),
                ('delivery_type', models.CharField(max_length=255)),
                ('assistance_measurement', models.CharField(max_length=255)),
                ('assistance_through', models.CharField(max_length=255)),
                ('vision_id', models.CharField(max_length=255)),
                ('funds_commitment', models.CharField(max_length=255)),
                ('down_payment', models.CharField(max_length=255)),
                ('validation_alerts_count', models.IntegerField()),
                ('total_persons_covered', models.IntegerField()),
                ('total_persons_covered_revised', models.IntegerField()),
                ('total_entitled_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_entitled_quantity_revised', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_delivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_undelivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('business_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.BusinessArea')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_plans', to='program.Program')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
