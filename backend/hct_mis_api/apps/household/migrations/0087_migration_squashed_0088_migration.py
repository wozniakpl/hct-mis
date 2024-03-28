# Generated by Django 3.2.24 on 2024-02-16 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('household', '0087_migration'), ('household', '0088_migration')]

    dependencies = [
        ('geo', '0004_migration'),
        ('household', '0003_migration_squashed_0086_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='admin_area_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='geo.area'),
        ),
        migrations.AlterModelOptions(
            name='household',
            options={'permissions': (('can_withdrawn', 'Can withdrawn Household'),), 'verbose_name': 'Household'},
        ),
        migrations.RenameField(
            model_name='household',
            old_name='female_age_group_0_4_count',
            new_name='female_age_group_0_5_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='female_age_group_0_4_disabled_count',
            new_name='female_age_group_0_5_disabled_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='female_age_group_13_17_count',
            new_name='female_age_group_12_17_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='female_age_group_13_17_disabled_count',
            new_name='female_age_group_12_17_disabled_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='female_age_group_5_12_count',
            new_name='female_age_group_6_11_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='female_age_group_5_12_disabled_count',
            new_name='female_age_group_6_11_disabled_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='male_age_group_0_4_count',
            new_name='male_age_group_0_5_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='male_age_group_0_4_disabled_count',
            new_name='male_age_group_0_5_disabled_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='male_age_group_13_17_count',
            new_name='male_age_group_12_17_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='male_age_group_13_17_disabled_count',
            new_name='male_age_group_12_17_disabled_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='male_age_group_5_12_count',
            new_name='male_age_group_6_11_count',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='male_age_group_5_12_disabled_count',
            new_name='male_age_group_6_11_disabled_count',
        ),
    ]
