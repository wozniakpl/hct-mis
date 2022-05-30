# Generated by Django 3.2.12 on 2022-05-05 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0062_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importedindividualidentity',
            options={'verbose_name_plural': 'Imported Individual Identities'},
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='mis_unicef_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='importedindividual',
            name='mis_unicef_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]