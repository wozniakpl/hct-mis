# Generated by Django 3.2.15 on 2022-09-29 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accountability', '0002_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackMessage',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('description', models.TextField(help_text='The content of the feedback message.', verbose_name='Description')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feedback_messages', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_messages', to='accountability.feedback')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
