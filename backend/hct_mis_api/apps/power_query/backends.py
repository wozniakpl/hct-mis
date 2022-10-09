from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.models import Permission

from ..account.models import Group, User, UserGroup
from .models import Query, Report, ReportDocument


class PowerQueryBackend(ModelBackend):
    def get_office_permissions(self, user_obj, office_slug):
        key = f"_perm_{office_slug}"
        if not hasattr(user_obj, key):
            perms = Permission.objects.filter(
                group__user_groups__user=user_obj, group__user_groups__business_area__slug=office_slug
            )
            perms = perms.values_list("content_type__app_label", "codename").order_by()
            setattr(user_obj, key, {"%s.%s" % (ct, name) for ct, name in perms})
        return getattr(user_obj, key)

    def has_perm(self, user_obj: User, perm, obj=None):
        # This is a bit tricky, HOPE permission system do not use standard Django
        # authorization mechanism. BusinessArea access is granted via "custom" system
        # where PowerQuery use default Django.
        if isinstance(obj, Report):
            if obj.owner == user_obj:
                return True
        elif isinstance(obj, ReportDocument):
            if obj.report.owner == user_obj:
                return True
            if "business_area" in obj.arguments:
                ba = obj.arguments["business_area"]
                return user_obj.is_active and perm in self.get_office_permissions(user_obj, ba)
        return None
