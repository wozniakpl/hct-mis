# Generated by Django 3.2.12 on 2022-04-05 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0036_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can_load_from_ad', 'Can load users from ActiveDirectory'), ('can_sync_with_ad', 'Can synchronise user with ActiveDirectory'), ('can_create_kobo_user', 'Can create users in Kobo'), ('can_import_from_kobo', 'Can import and sync users from Kobo'), ('can_upload_to_kobo', 'Can upload CSV file to Kobo'), ('can_debug', 'Can access debug informations'), ('can_inspect', 'Can inspect objects'), ('quick_links', 'Can see quick links in admin'))},
        ),
    ]
