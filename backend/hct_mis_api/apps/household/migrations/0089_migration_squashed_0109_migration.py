# Generated by Django 3.2.19 on 2023-06-10 13:19

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import multiselectfield.db.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    replaces = [('household', '0089_migration'), ('household', '0090_migration'), ('household', '0091_migration'), ('household', '0092_migration'), ('household', '0093_migration'), ('household', '0094_migration'), ('household', '0095_migration'), ('household', '0096_migration'), ('household', '0097_migration'), ('household', '0098_migration'), ('household', '0099_migration'), ('household', '0100_migration'), ('household', '0101_migration'), ('household', '0102_migration'), ('household', '0103_migration'), ('household', '0104_migration'), ('household', '0105_migration'), ('household', '0106_migration'), ('household', '0107_migration'), ('household', '0108_migration'), ('household', '0109_migration')]

    dependencies = [
        ('registration_data', '0018_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0043_migration'),
        ('household', '0088_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='row_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='individual',
            name='kobo_asset_id',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='individual',
            name='row_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='XlsxUpdateFile',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('file', models.FileField(upload_to='')),
                ('xlsx_match_columns', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), null=True, size=None)),
                ('business_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.businessarea')),
                ('rdi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration_data.registrationdataimport')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='agency',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='household',
            name='flex_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='household',
            name='user_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='deduplication_batch_results',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='deduplication_golden_record_results',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='flex_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='user_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individualidentity',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterModelOptions(
            name='documenttype',
            options={'ordering': ['country', 'label']},
        ),
        migrations.AlterModelOptions(
            name='individualidentity',
            options={'verbose_name_plural': 'Individual Identities'},
        ),
        migrations.AlterField(
            model_name='documenttype',
            name='type',
            field=models.CharField(choices=[('BIRTH_CERTIFICATE', 'Birth Certificate'), ('DRIVERS_LICENSE', "Driver's License"), ('ELECTORAL_CARD', 'Electoral Card'), ('NATIONAL_ID', 'National ID'), ('NATIONAL_PASSPORT', 'National Passport'), ('OTHER', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='household',
            name='consent_sharing',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('', 'None'), ('GOVERNMENT_PARTNER', 'Government partners'), ('HUMANITARIAN_PARTNER', 'Humanitarian partners'), ('PRIVATE_PARTNER', 'Private partners'), ('UNICEF', 'UNICEF')], default='', max_length=63),
        ),
        migrations.AlterField(
            model_name='household',
            name='org_enumerator',
            field=models.CharField(choices=[('', 'None'), ('PARTNER', 'Partner'), ('UNICEF', 'UNICEF')], default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='household',
            name='registration_method',
            field=models.CharField(choices=[('', 'None'), ('COMMUNITY', 'Community-level Registration'), ('HH_REGISTRATION', 'Household Registration')], default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='individual',
            name='comms_disability',
            field=models.CharField(blank=True, choices=[('', 'None'), ('LOT_DIFFICULTY', 'A lot of difficulty'), ('CANNOT_DO', 'Cannot do at all'), ('SOME_DIFFICULTY', 'Some difficulty')], max_length=50),
        ),
        migrations.AlterField(
            model_name='individual',
            name='deduplication_batch_status',
            field=models.CharField(choices=[('DUPLICATE_IN_BATCH', 'Duplicate in batch'), ('NOT_PROCESSED', 'Not Processed'), ('SIMILAR_IN_BATCH', 'Similar in batch'), ('UNIQUE_IN_BATCH', 'Unique in batch')], default='UNIQUE_IN_BATCH', max_length=50),
        ),
        migrations.AlterField(
            model_name='individual',
            name='deduplication_golden_record_status',
            field=models.CharField(choices=[('DUPLICATE', 'Duplicate'), ('NEEDS_ADJUDICATION', 'Needs Adjudication'), ('NOT_PROCESSED', 'Not Processed'), ('UNIQUE', 'Unique')], default='UNIQUE', max_length=50),
        ),
        migrations.AlterField(
            model_name='individual',
            name='hearing_disability',
            field=models.CharField(blank=True, choices=[('', 'None'), ('LOT_DIFFICULTY', 'A lot of difficulty'), ('CANNOT_DO', 'Cannot do at all'), ('SOME_DIFFICULTY', 'Some difficulty')], max_length=50),
        ),
        migrations.AlterField(
            model_name='individual',
            name='marital_status',
            field=models.CharField(choices=[('', 'None'), ('DIVORCED', 'Divorced'), ('MARRIED', 'Married'), ('SEPARATED', 'Separated'), ('SINGLE', 'Single'), ('WIDOWED', 'Widowed')], db_index=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='individual',
            name='memory_disability',
            field=models.CharField(blank=True, choices=[('', 'None'), ('LOT_DIFFICULTY', 'A lot of difficulty'), ('CANNOT_DO', 'Cannot do at all'), ('SOME_DIFFICULTY', 'Some difficulty')], max_length=50),
        ),
        migrations.AlterField(
            model_name='individual',
            name='physical_disability',
            field=models.CharField(blank=True, choices=[('', 'None'), ('LOT_DIFFICULTY', 'A lot of difficulty'), ('CANNOT_DO', 'Cannot do at all'), ('SOME_DIFFICULTY', 'Some difficulty')], max_length=50),
        ),
        migrations.AlterField(
            model_name='individual',
            name='relationship',
            field=models.CharField(blank=True, choices=[('UNKNOWN', 'Unknown'), ('AUNT_UNCLE', 'Aunt / Uncle'), ('BROTHER_SISTER', 'Brother / Sister'), ('COUSIN', 'Cousin'), ('DAUGHTERINLAW_SONINLAW', 'Daughter-in-law / Son-in-law'), ('GRANDDAUGHER_GRANDSON', 'Granddaughter / Grandson'), ('GRANDMOTHER_GRANDFATHER', 'Grandmother / Grandfather'), ('HEAD', 'Head of household (self)'), ('MOTHER_FATHER', 'Mother / Father'), ('MOTHERINLAW_FATHERINLAW', 'Mother-in-law / Father-in-law'), ('NEPHEW_NIECE', 'Nephew / Niece'), ('NON_BENEFICIARY', 'Not a Family Member. Can only act as a recipient.'), ('SISTERINLAW_BROTHERINLAW', 'Sister-in-law / Brother-in-law'), ('SON_DAUGHTER', 'Son / Daughter'), ('WIFE_HUSBAND', 'Wife / Husband')], help_text='This represents the MEMBER relationship. can be blank\n            as well if household is null!', max_length=255),
        ),
        migrations.AlterField(
            model_name='individual',
            name='seeing_disability',
            field=models.CharField(blank=True, choices=[('', 'None'), ('LOT_DIFFICULTY', 'A lot of difficulty'), ('CANNOT_DO', 'Cannot do at all'), ('SOME_DIFFICULTY', 'Some difficulty')], max_length=50),
        ),
        migrations.AlterField(
            model_name='individual',
            name='selfcare_disability',
            field=models.CharField(blank=True, choices=[('', 'None'), ('LOT_DIFFICULTY', 'A lot of difficulty'), ('CANNOT_DO', 'Cannot do at all'), ('SOME_DIFFICULTY', 'Some difficulty')], max_length=50),
        ),
        migrations.AlterField(
            model_name='individualroleinhousehold',
            name='role',
            field=models.CharField(blank=True, choices=[('NO_ROLE', 'None'), ('ALTERNATE', 'Alternate collector'), ('PRIMARY', 'Primary collector')], max_length=255),
        ),
        migrations.AlterField(
            model_name='household',
            name='residence_status',
            field=models.CharField(choices=[('', 'None'), ('IDP', 'Displaced  |  Internally Displaced People'), ('REFUGEE', 'Displaced  |  Refugee / Asylum Seeker'), ('OTHERS_OF_CONCERN', 'Displaced  |  Others of Concern'), ('HOST', 'Non-displaced  |   Host'), ('NON_HOST', 'Non-displaced  |   Non-host')], max_length=254),
        ),
        migrations.AlterField(
            model_name='household',
            name='is_removed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='individual',
            name='is_removed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='documenttype',
            name='type',
            field=models.CharField(choices=[('BIRTH_CERTIFICATE', 'Birth Certificate'), ('DRIVERS_LICENSE', "Driver's License"), ('ELECTORAL_CARD', 'Electoral Card'), ('NATIONAL_ID', 'National ID'), ('NATIONAL_PASSPORT', 'National Passport'), ('TAX_ID', 'Tax Number Identification'), ('RESIDENCE_PERMIT_NO', "Foreigner's Residence Permit"), ('OTHER', 'Other')], max_length=50),
        ),
        migrations.AddField(
            model_name='individual',
            name='disability_certificate_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='individual',
            name='relationship',
            field=models.CharField(blank=True, choices=[('UNKNOWN', 'Unknown'), ('AUNT_UNCLE', 'Aunt / Uncle'), ('BROTHER_SISTER', 'Brother / Sister'), ('COUSIN', 'Cousin'), ('DAUGHTERINLAW_SONINLAW', 'Daughter-in-law / Son-in-law'), ('GRANDDAUGHER_GRANDSON', 'Granddaughter / Grandson'), ('GRANDMOTHER_GRANDFATHER', 'Grandmother / Grandfather'), ('HEAD', 'Head of household (self)'), ('MOTHER_FATHER', 'Mother / Father'), ('MOTHERINLAW_FATHERINLAW', 'Mother-in-law / Father-in-law'), ('NEPHEW_NIECE', 'Nephew / Niece'), ('NON_BENEFICIARY', 'Not a Family Member. Can only act as a recipient.'), ('OTHER', 'Other'), ('SISTERINLAW_BROTHERINLAW', 'Sister-in-law / Brother-in-law'), ('SON_DAUGHTER', 'Son / Daughter'), ('WIFE_HUSBAND', 'Wife / Husband')], help_text='This represents the MEMBER relationship. can be blank\n            as well if household is null!', max_length=255),
        ),
        migrations.CreateModel(
            name='BankAccountInfo',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('is_removed', models.BooleanField(db_index=True, default=False)),
                ('removed_date', models.DateTimeField(blank=True, null=True)),
                ('last_sync_at', models.DateTimeField(blank=True, null=True)),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_account_number', models.CharField(max_length=64)),
                ('debit_card_number', models.CharField(blank=True, default='', max_length=255)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_account_info', to='household.individual')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='individual',
            name='sanction_list_last_check',
        ),
        migrations.AlterField(
            model_name='individual',
            name='sanction_list_confirmed_match',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='individual',
            name='sanction_list_possible_match',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='household',
            name='children_count',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='children_disabled_count',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='female_children_count',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='female_children_disabled_count',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='male_children_count',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='male_children_disabled_count',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='total_cash_received',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='total_cash_received_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True),
        ),
        migrations.AlterField(
            model_name='household',
            name='address',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='individual',
            name='phone_no',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='individual',
            name='phone_no_alternative',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='household',
            name='kobo_asset_id',
            field=models.CharField(blank=True, db_index=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='individual',
            name='deduplication_golden_record_status',
            field=models.CharField(choices=[('DUPLICATE', 'Duplicate'), ('NEEDS_ADJUDICATION', 'Needs Adjudication'), ('NOT_PROCESSED', 'Not Processed'), ('POSTPONE', 'Postpone'), ('UNIQUE', 'Unique')], default='UNIQUE', max_length=50),
        ),
    ]
