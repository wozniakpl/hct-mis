# Generated by Django 2.2.16 on 2021-09-17 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0044_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='female_age_group_0_5_count',
            new_name='female_age_group_0_4_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='female_age_group_0_5_disabled_count',
            new_name='female_age_group_0_4_disabled_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='female_age_group_12_17_count',
            new_name='female_age_group_13_17_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='female_age_group_12_17_disabled_count',
            new_name='female_age_group_13_17_disabled_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='female_age_group_6_11_count',
            new_name='female_age_group_5_12_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='female_age_group_6_11_disabled_count',
            new_name='female_age_group_5_12_disabled_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='male_age_group_0_5_count',
            new_name='male_age_group_0_4_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='male_age_group_0_5_disabled_count',
            new_name='male_age_group_0_4_disabled_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='male_age_group_12_17_count',
            new_name='male_age_group_13_17_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='male_age_group_12_17_disabled_count',
            new_name='male_age_group_13_17_disabled_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='male_age_group_6_11_count',
            new_name='male_age_group_5_12_count',
        ),
        migrations.RenameField(
            model_name='importedhousehold',
            old_name='male_age_group_6_11_disabled_count',
            new_name='male_age_group_5_12_disabled_count',
        ),
    ]
