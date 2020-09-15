from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import UUIDModel

from utils.models import TimeStampedUUIDModel


class User(AbstractUser, UUIDModel):
    business_areas = models.ManyToManyField("core.BusinessArea", blank=True)
    roles = models.ManyToManyField("account.UserRole", blank=True, related_name="users")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserRole(TimeStampedUUIDModel):
    name = models.CharField(max_length=250)
    business_area = models.ForeignKey("core.BusinessArea", on_delete=models.CASCADE)
    permissions = models.ManyToManyField("account.UserPermission", related_name="roles")

    def __str__(self):
        return f"{self.name} in {self.business_area}"


class UserPermission(TimeStampedUUIDModel):
    PERMISSION_DASHBOARD = 1
    PERMISSION_RDI = 2
    PERMISSION_POPULATION = 3
    PERMISSION_PROGRAM_MANAGEMENT = 4
    PERMISSION_TARGETING = 5
    PERMISSION_PAYMENT_VERIFICATION = 6
    PERMISSION_GRIEVANCES = 7
    PERMISSION_REPORTING = 8
    PERMISSION_USER_MANAGEMENT = 9
    PERMISSION_SETTINGS = 10
    PERMISSIONS_CHOICES = (
        (PERMISSION_DASHBOARD, _("Dashboard")),
        (PERMISSION_RDI, _("Registration Data Import")),
        (PERMISSION_POPULATION, _("Population")),
        (PERMISSION_PROGRAM_MANAGEMENT, _("Program Management")),
        (PERMISSION_TARGETING, _("Targeting")),
        (PERMISSION_PAYMENT_VERIFICATION, _("Payment Verification")),
        (PERMISSION_REPORTING, _("Reporting")),
        (PERMISSION_USER_MANAGEMENT, _("User Management")),
        (PERMISSION_SETTINGS, _("Settings")),
    )
    PERMISSIONS_CHOICES_DICT = dict(PERMISSIONS_CHOICES)
    name = models.CharField(max_length=250, choices=PERMISSIONS_CHOICES)
    write = models.BooleanField(default=False)

    def __str__(self):
        type_name = _("Read")
        if self.write:
            type_name = _("Write")
        return f"{UserPermission.PERMISSIONS_CHOICES_DICT.get(int(self.name))} {type_name} Permission"
