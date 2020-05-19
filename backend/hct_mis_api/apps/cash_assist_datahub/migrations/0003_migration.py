# Generated by Django 2.2.8 on 2020-05-19 13:45

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cash_assist_datahub', '0002_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashPlan',
            fields=[
                ('business_area', models.CharField(max_length=20)),
                ('cash_plan_id', models.CharField(max_length=255)),
                ('cash_plan_hash_id', models.UUIDField(primary_key=True, serialize=False)),
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
                ('payment_records_count', models.IntegerField()),
                ('total_entitled_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_entitled_quantity_revised', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_delivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_undelivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('household_id', models.UUIDField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('INACTIVE', 'Inactive'), ('ACTIVE', 'Active')], max_length=50)),
                ('household_size', models.PositiveIntegerField()),
                ('government_form_number', models.CharField(max_length=255, null=True)),
                ('form_number', models.CharField(max_length=255, null=True)),
                ('agency_id', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('admin1', models.CharField(max_length=255, null=True)),
                ('admin2', models.CharField(max_length=255, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('individual_id', models.UUIDField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('INACTIVE', 'Inactive'), ('ACTIVE', 'Active')], max_length=50, null=True)),
                ('full_name', models.CharField(max_length=255)),
                ('family_name', models.CharField(max_length=255, null=True)),
                ('given_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True)),
                ('sex', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=255)),
                ('date_of_birth', models.DateField()),
                ('estimated_date_of_birth', models.BooleanField()),
                ('relationship', models.CharField(choices=[('NON_BENEFICIARY', 'Not a Family Member. Can only act as a recipient.'), ('HEAD', 'Head of household (self)'), ('SON_DAUGHTER', 'Son / Daughter'), ('WIFE_HUSBAND', 'Wife / Husband'), ('BROTHER_SISTER', 'Brother / Sister'), ('MOTHER_FATHER', 'Mother / Father'), ('AUNT_UNCLE', 'Aunt / Uncle'), ('GRANDMOTHER_GRANDFATHER', 'Grandmother / Grandfather'), ('MOTHERINLAW_FATHERINLAW', 'Mother-in-law / Father-in-law'), ('DAUGHTERINLAW_SONINLAW', 'Daughter-in-law / Son-in-law'), ('SISTERINLAW_BROTHERINLAW', 'Sister-in-law / Brother-in-law'), ('GRANDDAUGHER_GRANDSON', 'Granddaughter / Grandson'), ('NEPHEW_NIECE', 'Nephew / Niece'), ('COUSIN', 'Cousin')], max_length=255, null=True)),
                ('role', models.CharField(choices=[('PRIMARY', 'Primary collector'), ('ALTERNATE', 'Alternate collector'), ('NO_ROLE', 'None')], max_length=255, null=True)),
                ('marital_status', models.CharField(choices=[('SINGLE', 'SINGLE'), ('MARRIED', 'Married'), ('WIDOW', 'Widow'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated')], max_length=255)),
                ('phone_number', models.CharField(max_length=14, null=True)),
                ('household', models.ForeignKey(db_column='household_id', on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Household')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('program_id', models.UUIDField(primary_key=True, serialize=False)),
                ('business_area', models.CharField(max_length=20)),
                ('program_unhcr_id', models.CharField(max_length=255)),
                ('program_hash_id', models.CharField(max_length=255)),
                ('programme_name', models.CharField(max_length=255)),
                ('scope', models.PositiveIntegerField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('description', models.CharField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(choices=[('MIS', 'HCT-MIS'), ('CA', 'Cash Assist')], max_length=3)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('READY', 'Ready'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], max_length=11)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TargetPopulation',
            fields=[
                ('tp_unicef_id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('population_type', models.CharField(default='HOUSEHOLD', max_length=20)),
                ('targeting_criteria', models.TextField()),
                ('active_households', models.PositiveIntegerField(default=0)),
                ('program', models.ForeignKey(db_column='program_id', on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Program')),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TargetPopulationEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unhcr_household_id', models.CharField(max_length=255)),
                ('vulnerability_score', models.DecimalField(blank=True, decimal_places=3, help_text='Written by a tool such as Corticon.', max_digits=6, null=True)),
                ('household', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Household')),
                ('individual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Individual')),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
                ('target_population', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.TargetPopulation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('business_area', models.CharField(max_length=20)),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=4)),
                ('country', models.CharField(max_length=3)),
                ('vision_id', models.CharField(max_length=255)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='program',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session'),
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('business_area', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('SUCCESS', 'Sucess'), ('PENDING', 'Pending'), ('ERROR', 'Error')], max_length=255)),
                ('status_date', models.DateTimeField()),
                ('payment_id', models.CharField(max_length=255)),
                ('payment_hash_id', models.UUIDField(primary_key=True, serialize=False)),
                ('unhcr_registration_id', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('total_persons_covered', models.IntegerField()),
                ('distribution_modality', models.CharField(max_length=255)),
                ('target_population_cash_assist_id', models.CharField(max_length=255)),
                ('entitlement_card_number', models.CharField(max_length=255)),
                ('entitlement_card_status', models.CharField(choices=[('SUCCESS', 'Sucess'), ('PENDING', 'Pending'), ('ERROR', 'Error')], default='ACTIVE', max_length=20)),
                ('entitlement_card_issue_date', models.DateField()),
                ('delivery_type', models.CharField(choices=[('CASH', 'Cash'), ('DEPOSIT_TO_CARD', 'Deposit to Card'), ('TRANSFER', 'Transfer')], default='ACTIVE', max_length=20)),
                ('currency', models.CharField(max_length=4)),
                ('entitlement_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('delivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('delivery_date', models.DateTimeField()),
                ('cash_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='cash_assist_datahub.CashPlan')),
                ('focal_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='cash_assist_datahub.Individual')),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='cash_assist_datahub.Household')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='cash_assist_datahub.ServiceProvider')),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
                ('target_population', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='cash_assist_datahub.TargetPopulation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='individual',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session'),
        ),
        migrations.AddField(
            model_name='household',
            name='focal_point',
            field=models.ForeignKey(db_column='focal_point', on_delete=django.db.models.deletion.CASCADE, related_name='heading_household', to='cash_assist_datahub.Individual'),
        ),
        migrations.AddField(
            model_name='household',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session'),
        ),
        migrations.AddField(
            model_name='cashplan',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_plans', to='cash_assist_datahub.Program'),
        ),
        migrations.AddField(
            model_name='cashplan',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session'),
        ),
    ]
