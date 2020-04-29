# Generated by Django 2.2.8 on 2020-04-29 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationDataImport',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('IN_REVIEW', 'In Review'), ('APPROVED', 'Approved'), ('MERGED', 'Merged'), ('MERGING', 'Merging')], default='IN_REVIEW', max_length=255)),
                ('import_date', models.DateTimeField(auto_now_add=True)),
                ('data_source', models.CharField(choices=[('XLS', 'Excel'), ('3RD_PARTY', '3rd party'), ('XML', 'XML'), ('OTHER', 'Other')], max_length=255)),
                ('number_of_individuals', models.PositiveIntegerField()),
                ('number_of_households', models.PositiveIntegerField()),
                ('datahub_id', models.UUIDField(default=None, null=True)),
                ('business_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.BusinessArea')),
                ('imported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_data_imports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
