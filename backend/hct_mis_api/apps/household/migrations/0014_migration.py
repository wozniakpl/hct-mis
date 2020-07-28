# Generated by Django 2.2.8 on 2020-07-21 22:31

from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0013_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individual',
            name='role',
        ),
        migrations.AlterField(
            model_name='individual',
            name='household',
            field=models.ForeignKey(blank=True, help_text='This represents the household this person is a MEMBER,\n            and if null then relationship is NON_BENEFICIARY and that\n            simply means they are a representative of one or more households\n            and not a member of one.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individuals', to='household.Household'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='relationship',
            field=models.CharField(blank=True, choices=[('NON_BENEFICIARY', 'Not a Family Member. Can only act as a recipient.'), ('HEAD', 'Head of household (self)'), ('SON_DAUGHTER', 'Son / Daughter'), ('WIFE_HUSBAND', 'Wife / Husband'), ('BROTHER_SISTER', 'Brother / Sister'), ('MOTHER_FATHER', 'Mother / Father'), ('AUNT_UNCLE', 'Aunt / Uncle'), ('GRANDMOTHER_GRANDFATHER', 'Grandmother / Grandfather'), ('MOTHERINLAW_FATHERINLAW', 'Mother-in-law / Father-in-law'), ('DAUGHTERINLAW_SONINLAW', 'Daughter-in-law / Son-in-law'), ('SISTERINLAW_BROTHERINLAW', 'Sister-in-law / Brother-in-law'), ('GRANDDAUGHER_GRANDSON', 'Granddaughter / Grandson'), ('NEPHEW_NIECE', 'Nephew / Niece'), ('COUSIN', 'Cousin')], help_text='This represents the MEMBER relationship. can be blank\n            as well if household is null!', max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='IndividualRoleInHousehold',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_sync_at', models.DateTimeField(null=True)),
                ('role', models.CharField(blank=True, choices=[('PRIMARY', 'Primary collector'), ('ALTERNATE', 'Alternate collector'), ('NO_ROLE', 'None')], max_length=255)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='individuals_and_roles', to='household.Household')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='households_and_roles', to='household.Individual')),
            ],
            options={
                'unique_together': {('role', 'household')},
            },
        ),
        migrations.AddField(
            model_name='household',
            name='representatives',
            field=models.ManyToManyField(help_text='This is only used to track collector (primary or secondary) of a household.\n            They may still be a HOH of this household or any other household.\n            Through model will contain the role (ROLE_CHOICE) they are connected with on.', related_name='represented_households', through='household.IndividualRoleInHousehold', to='household.Individual'),
        ),
    ]
