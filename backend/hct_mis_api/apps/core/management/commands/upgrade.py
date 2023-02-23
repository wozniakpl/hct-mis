from typing import Any

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        call_command("collectstatic", interactive=False)
        call_command("migratealldb")
        call_command("generateroles")
        from adminactions.perms import create_extra_permissions

        try:
            create_extra_permissions()
        except AttributeError:
            # kinda hacky but this is the only way for now to make it work
            # first time, we get AttributeError: 'NoneType' object has no attribute '_meta'
            # but the second time, we don't
            create_extra_permissions()

        from hct_mis_api.apps.power_query.defaults import create_defaults

        create_defaults()
