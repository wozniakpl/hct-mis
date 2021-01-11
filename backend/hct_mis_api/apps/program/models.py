from decimal import Decimal

from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from cash_assist_datahub.models import PaymentRecord
from payment.models import CashPlanPaymentVerification
from utils.models import AbstractSyncable, TimeStampedUUIDModel, ConcurrencyModel


class Program(TimeStampedUUIDModel, AbstractSyncable, ConcurrencyModel):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    STATUS_CHOICE = (
        (DRAFT, _("Draft")),
        (ACTIVE, _("Active")),
        (FINISHED, _("Finished")),
    )

    REGULAR = "REGULAR"
    ONE_OFF = "ONE_OFF"

    FREQUENCY_OF_PAYMENTS_CHOICE = (
        (REGULAR, _("Regular")),
        (ONE_OFF, _("One-off")),
    )

    CHILD_PROTECTION = "CHILD_PROTECTION"
    EDUCATION = "EDUCATION"
    HEALTH = "HEALTH"
    MULTI_PURPOSE = "MULTI_PURPOSE"
    NUTRITION = "NUTRITION"
    SOCIAL_POLICY = "SOCIAL_POLICY"
    WASH = "WASH"

    SECTOR_CHOICE = (
        (CHILD_PROTECTION, _("Child Protection")),
        (EDUCATION, _("Education")),
        (HEALTH, _("Health")),
        (MULTI_PURPOSE, _("Multi Purpose")),
        (NUTRITION, _("Nutrition")),
        (SOCIAL_POLICY, _("Social Policy")),
        (WASH, _("WASH")),
    )

    SCOPE_FOR_PARTNERS = "FOR_PARTNERS"
    SCOPE_UNICEF = "UNICEF"

    SCOPE_CHOICE = (
        (SCOPE_FOR_PARTNERS, _("For partners")),
        (SCOPE_UNICEF, _("Unicef")),
    )

    name = models.CharField(max_length=255, validators=[MinLengthValidator(3), MaxLengthValidator(255)],)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE,)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=255, validators=[MinLengthValidator(3), MaxLengthValidator(255)],)
    ca_id = models.CharField(max_length=255, null=True)
    ca_hash_id = models.CharField(max_length=255, null=True)
    admin_areas = models.ManyToManyField("core.AdminArea", related_name="programs", blank=True,)
    business_area = models.ForeignKey("core.BusinessArea", on_delete=models.CASCADE)
    budget = models.DecimalField(decimal_places=2, max_digits=11, validators=[MinValueValidator(Decimal("0.00"))],)
    frequency_of_payments = models.CharField(max_length=50, choices=FREQUENCY_OF_PAYMENTS_CHOICE,)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICE,)
    scope = models.CharField(max_length=50, choices=SCOPE_CHOICE,)
    cash_plus = models.BooleanField()
    population_goal = models.PositiveIntegerField()
    administrative_areas_of_implementation = models.CharField(
        max_length=255, validators=[MinLengthValidator(3), MaxLengthValidator(255)],
    )
    history = AuditlogHistoryField(pk_indexable=False)
    individual_data_needed = models.BooleanField(
        default=False,
        help_text="""
        This boolean decides whether the target population sync will send
        all individuals of a household thats part of the population or only
        the relevant ones (collectors etc.)""",
    )

    @property
    def total_number_of_households(self):
        return self.cash_plans.aggregate(households=Coalesce(Sum("total_persons_covered"), 0),)["households"]

    class Meta:
        unique_together = ("name", "business_area")


class CashPlan(TimeStampedUUIDModel):
    DISTRIBUTION_COMPLETED = "Distribution Completed"
    DISTRIBUTION_COMPLETED_WITH_ERRORS = "Distribution Completed with Errors"
    TRANSACTION_COMPLETED = "Transaction Completed"
    TRANSACTION_COMPLETED_WITH_ERRORS = "Transaction Completed with Errors"

    STATUS_CHOICE = (
        (DISTRIBUTION_COMPLETED, _("Distribution Completed")),
        (DISTRIBUTION_COMPLETED_WITH_ERRORS, _("Distribution Completed with Errors"),),
        (TRANSACTION_COMPLETED, _("Transaction Completed")),
        (TRANSACTION_COMPLETED_WITH_ERRORS, _("Transaction Completed with Errors"),),
    )
    business_area = models.ForeignKey("core.BusinessArea", on_delete=models.CASCADE)
    ca_id = models.CharField(max_length=255, null=True)
    ca_hash_id = models.UUIDField(unique=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICE)
    status_date = models.DateTimeField()
    name = models.CharField(max_length=255)
    distribution_level = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    dispersion_date = models.DateTimeField()
    coverage_duration = models.PositiveIntegerField()
    coverage_unit = models.CharField(max_length=255)
    comments = models.CharField(max_length=255, null=True)
    program = models.ForeignKey("program.Program", on_delete=models.CASCADE, related_name="cash_plans")
    delivery_type = models.CharField(choices=PaymentRecord.DELIVERY_TYPE_CHOICE, max_length=20, blank=True)
    assistance_measurement = models.CharField(max_length=255)
    assistance_through = models.CharField(max_length=255)
    vision_id = models.CharField(max_length=255)
    funds_commitment = models.CharField(max_length=255)
    down_payment = models.CharField(max_length=255)
    validation_alerts_count = models.IntegerField()
    total_persons_covered = models.IntegerField()
    total_persons_covered_revised = models.IntegerField()
    total_entitled_quantity = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal("0.01"))],
    )
    total_entitled_quantity_revised = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal("0.01"))],
    )
    total_delivered_quantity = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal("0.01"))],
    )
    total_undelivered_quantity = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal("0.01"))],
    )
    verification_status = models.CharField(
        max_length=10,
        default=CashPlanPaymentVerification.STATUS_PENDING,
        choices=CashPlanPaymentVerification.STATUS_CHOICES,
    )

    @property
    def payment_records_count(self):
        return self.payment_records.count()

    @property
    def bank_reconciliation_success(self):
        return self.payment_records.filter(status=PaymentRecord.STATUS_SUCCESS).count()

    @property
    def bank_reconciliation_error(self):
        return self.payment_records.filter(status=PaymentRecord.STATUS_ERROR).count()


auditlog.register(Program)

auditlog.register(CashPlan)
