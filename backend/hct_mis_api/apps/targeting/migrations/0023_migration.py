# Generated by Django 2.2.16 on 2021-11-04 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('targeting', '0022_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='targetpopulation',
            old_name='approved_at',
            new_name='change_date',
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='locked_target_populations', to=settings.AUTH_USER_MODEL),
        ),
    ]
