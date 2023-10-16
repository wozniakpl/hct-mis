# Generated by Django 3.2.20 on 2023-09-23 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='migrationstatus',
            options={'verbose_name_plural': 'Migration Status'},
        ),
        migrations.AddField(
            model_name='datacollectingtype',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='datacollectingtype',
            name='individual_filters_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='datacollectingtype',
            name='limit_to',
            field=models.ManyToManyField(related_name='data_collecting_types', to='core.BusinessArea'),
        ),
    ]