from datetime import timedelta
from decimal import Decimal
from random import randint
from uuid import UUID

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

import factory
from pytz import utc

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.account.models import User
from hct_mis_api.apps.core.currencies import CURRENCY_CHOICES
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.core.utils import CaIdIterator
from hct_mis_api.apps.geo.models import Area
from hct_mis_api.apps.household.fixtures import (
    EntitlementCardFactory,
    HouseholdFactory,
    IndividualFactory,
    IndividualRoleInHouseholdFactory,
    create_household,
)
from hct_mis_api.apps.household.models import (
    MALE,
    REFUGEE,
    ROLE_PRIMARY,
    Household,
    Individual,
)
from hct_mis_api.apps.payment.models import (
    CashPlan,
    DeliveryMechanismPerPaymentPlan,
    FinancialServiceProvider,
    FinancialServiceProviderXlsxReport,
    FinancialServiceProviderXlsxTemplate,
    GenericPayment,
    Payment,
    PaymentChannel,
    PaymentPlan,
    PaymentRecord,
    PaymentVerification,
    PaymentVerificationPlan,
    PaymentVerificationSummary,
    ServiceProvider,
)
from hct_mis_api.apps.program.fixtures import ProgramFactory
from hct_mis_api.apps.program.models import Program
from hct_mis_api.apps.registration_data.fixtures import RegistrationDataImportFactory
from hct_mis_api.apps.targeting.fixtures import (
    TargetingCriteriaFactory,
    TargetPopulationFactory,
)
from hct_mis_api.apps.targeting.models import (
    TargetingCriteria,
    TargetingCriteriaRule,
    TargetingCriteriaRuleFilter,
    TargetPopulation,
)


class PaymentVerificationSummaryFactory(factory.DjangoModelFactory):
    class Meta:
        model = PaymentVerificationSummary


class CashPlanFactory(factory.DjangoModelFactory):
    class Meta:
        model = CashPlan

    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    program = factory.SubFactory(ProgramFactory)
    status_date = factory.Faker(
        "date_time_this_decade",
        before_now=False,
        after_now=True,
        tzinfo=utc,
    )
    status = factory.fuzzy.FuzzyChoice(
        CashPlan.STATUS_CHOICE,
        getter=lambda c: c[0],
    )
    name = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True,
        ext_word_list=None,
    )
    distribution_level = "Registration Group"
    start_date = factory.Faker(
        "date_time_this_decade",
        before_now=False,
        after_now=True,
        tzinfo=utc,
    )
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=randint(60, 1000)))
    dispersion_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=randint(60, 1000)))
    coverage_duration = factory.fuzzy.FuzzyInteger(1, 4)
    coverage_unit = factory.Faker(
        "random_element",
        elements=["Day(s)", "Week(s)", "Month(s)", "Year(s)"],
    )
    comments = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True,
        ext_word_list=None,
    )
    delivery_type = factory.fuzzy.FuzzyChoice(
        PaymentRecord.DELIVERY_TYPE_CHOICE,
        getter=lambda c: c[0],
    )
    assistance_measurement = factory.Faker("currency_name")
    assistance_through = factory.Faker("random_element", elements=["ING", "Bank of America", "mBank"])
    vision_id = factory.Faker("uuid4")
    funds_commitment = factory.fuzzy.FuzzyInteger(1000, 99999999)
    exchange_rate = factory.fuzzy.FuzzyDecimal(0.1, 9.9)
    down_payment = factory.fuzzy.FuzzyInteger(1000, 99999999)
    validation_alerts_count = factory.fuzzy.FuzzyInteger(1, 3)
    total_persons_covered = factory.fuzzy.FuzzyInteger(1, 4)
    total_persons_covered_revised = factory.fuzzy.FuzzyInteger(1, 4)

    total_entitled_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_entitled_quantity_revised = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_delivered_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_undelivered_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)

    total_entitled_quantity_usd = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_entitled_quantity_revised_usd = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_delivered_quantity_usd = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_undelivered_quantity_usd = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)

    @factory.post_generation
    def payment_verification_summary(self, create, extracted, **kwargs):
        if not create:
            return

        PaymentVerificationSummaryFactory(payment_plan=self)


class ServiceProviderFactory(factory.DjangoModelFactory):
    class Meta:
        model = ServiceProvider

    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    ca_id = factory.Iterator(CaIdIterator("SRV"))
    full_name = factory.Faker("company")
    short_name = factory.LazyAttribute(lambda o: o.full_name[0:3])
    country = factory.Faker("country_code")
    vision_id = factory.fuzzy.FuzzyInteger(1342342, 9999999932)


class FinancialServiceProviderXlsxTemplateFactory(factory.DjangoModelFactory):
    class Meta:
        model = FinancialServiceProviderXlsxTemplate

    name = factory.Faker("name")
    columns = FinancialServiceProviderXlsxTemplate.DEFAULT_COLUMNS


class FinancialServiceProviderFactory(factory.DjangoModelFactory):
    class Meta:
        model = FinancialServiceProvider

    name = factory.Faker("company")
    vision_vendor_number = factory.Faker("ssn")
    delivery_mechanisms = factory.List(
        [
            factory.fuzzy.FuzzyChoice(
                GenericPayment.DELIVERY_TYPE_CHOICE,
                getter=lambda c: c[0],
            )
        ]
    )
    distribution_limit = factory.fuzzy.FuzzyDecimal(pow(10, 5), pow(10, 6))
    communication_channel = factory.fuzzy.FuzzyChoice(
        FinancialServiceProvider.COMMUNICATION_CHANNEL_CHOICES, getter=lambda c: c[0]
    )
    data_transfer_configuration = factory.Faker("json")
    fsp_xlsx_template = factory.SubFactory(FinancialServiceProviderXlsxTemplateFactory)


class PaymentChannelFactory(factory.DjangoModelFactory):
    class Meta:
        model = PaymentChannel

    individual = factory.SubFactory(IndividualFactory)
    delivery_mechanism = factory.fuzzy.FuzzyChoice(GenericPayment.DELIVERY_TYPE_CHOICE, getter=lambda c: c[0])
    delivery_data = factory.Faker("json")


class FinancialServiceProviderXlsxReportFactory(factory.DjangoModelFactory):
    class Meta:
        model = FinancialServiceProviderXlsxReport

    financial_service_provider = factory.SubFactory(FinancialServiceProviderFactory)


class PaymentRecordFactory(factory.DjangoModelFactory):
    class Meta:
        model = PaymentRecord

    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    status = factory.fuzzy.FuzzyChoice(
        PaymentRecord.STATUS_CHOICE,
        getter=lambda c: c[0],
    )
    full_name = factory.Faker("name")
    status_date = factory.Faker(
        "date_time_this_decade",
        before_now=False,
        after_now=True,
        tzinfo=utc,
    )
    ca_id = factory.Iterator(CaIdIterator("PR"))
    ca_hash_id = factory.Faker("uuid4")
    parent = factory.SubFactory(CashPlanFactory)
    household = factory.SubFactory(HouseholdFactory)
    total_persons_covered = factory.fuzzy.FuzzyInteger(1, 7)
    distribution_modality = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True,
        ext_word_list=None,
    )
    target_population = factory.SubFactory(TargetPopulationFactory)
    entitlement_card_number = factory.Faker("ssn")
    entitlement_card_status = factory.fuzzy.FuzzyChoice(
        PaymentRecord.ENTITLEMENT_CARD_STATUS_CHOICE,
        getter=lambda c: c[0],
    )
    entitlement_card_issue_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    delivery_type = factory.fuzzy.FuzzyChoice(
        PaymentRecord.DELIVERY_TYPE_CHOICE,
        getter=lambda c: c[0],
    )
    currency = factory.Faker("currency_code")
    entitlement_quantity = factory.fuzzy.FuzzyDecimal(100.0, 10000.0)
    delivered_quantity = factory.fuzzy.FuzzyDecimal(100.0, 10000.0)
    delivered_quantity_usd = factory.fuzzy.FuzzyDecimal(100.0, 10000.0)
    delivery_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    service_provider = factory.SubFactory(ServiceProviderFactory)
    registration_ca_id = factory.Faker("uuid4")


class PaymentVerificationPlanFactory(factory.DjangoModelFactory):
    status = factory.fuzzy.FuzzyChoice(
        ((PaymentVerificationPlan.STATUS_PENDING, "pending"),),
        getter=lambda c: c[0],
    )
    sampling = factory.fuzzy.FuzzyChoice(
        PaymentVerificationPlan.SAMPLING_CHOICES,
        getter=lambda c: c[0],
    )
    verification_channel = factory.fuzzy.FuzzyChoice(
        PaymentVerificationPlan.VERIFICATION_CHANNEL_CHOICES,
        getter=lambda c: c[0],
    )
    sample_size = factory.fuzzy.FuzzyInteger(0, 100)
    responded_count = factory.fuzzy.FuzzyInteger(20, 90)
    received_count = factory.fuzzy.FuzzyInteger(30, 70)
    not_received_count = factory.fuzzy.FuzzyInteger(0, 10)
    received_with_problems_count = factory.fuzzy.FuzzyInteger(0, 10)
    rapid_pro_flow_start_uuids = factory.LazyFunction(list)

    class Meta:
        model = PaymentVerificationPlan

    @factory.post_generation
    def add_payment_plan_obj(obj, create, extracted, **kwargs):
        if not create:
            return

        if not obj.payment_plan_object_id and not obj.payment_plan_content_type:
            cash_plan_ct, _ = ContentType.objects.get_or_create(app_label="payment", model="cashplan")
            obj.payment_plan_object_id = CashPlanFactory().pk
            obj.payment_plan_content_type = cash_plan_ct
            obj.save()


class PaymentVerificationFactory(factory.DjangoModelFactory):
    payment_verification_plan = factory.Iterator(
        PaymentVerificationPlan.objects.filter(
            payment_plan_content_type=ContentType.objects.get(app_label="payment", model="cashplan")
        )
    )
    status = factory.fuzzy.FuzzyChoice(
        PaymentVerification.STATUS_CHOICES,
        getter=lambda c: c[0],
    )
    status_date = factory.Faker("date_time_this_year", before_now=True, after_now=False, tzinfo=utc)

    class Meta:
        model = PaymentVerification

    @factory.post_generation
    def add_payment_obj(obj, create, extracted, **kwargs):
        if not create:
            return

        if not obj.payment_object_id and not obj.payment_content_type:
            cash_plan_ct, _ = ContentType.objects.get_or_create(app_label="payment", model="paymentrecord")
            obj.payment_object_id = PaymentRecordFactory().pk
            obj.payment_content_type = cash_plan_ct
            obj.save()


class RealProgramFactory(factory.DjangoModelFactory):
    class Meta:
        model = Program

    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    ca_id = factory.Iterator(CaIdIterator("PRG"))
    name = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True,
        ext_word_list=None,
    )
    status = factory.fuzzy.FuzzyChoice(
        Program.STATUS_CHOICE,
        getter=lambda c: c[0],
    )
    start_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=randint(60, 1000)))
    description = factory.Faker(
        "sentence",
        nb_words=10,
        variable_nb_words=True,
        ext_word_list=None,
    )
    budget = factory.fuzzy.FuzzyDecimal(1000000.0, 900000000.0)
    frequency_of_payments = factory.fuzzy.FuzzyChoice(
        Program.FREQUENCY_OF_PAYMENTS_CHOICE,
        getter=lambda c: c[0],
    )
    sector = factory.fuzzy.FuzzyChoice(
        Program.SECTOR_CHOICE,
        getter=lambda c: c[0],
    )
    scope = factory.fuzzy.FuzzyChoice(
        Program.SCOPE_CHOICE,
        getter=lambda c: c[0],
    )
    cash_plus = factory.fuzzy.FuzzyChoice((True, False))
    population_goal = factory.fuzzy.FuzzyDecimal(50000.0, 600000.0)
    administrative_areas_of_implementation = factory.Faker(
        "sentence",
        nb_words=3,
        variable_nb_words=True,
        ext_word_list=None,
    )
    individual_data_needed = factory.fuzzy.FuzzyChoice((True, False))


class RealCashPlanFactory(factory.DjangoModelFactory):
    class Meta:
        model = CashPlan

    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    ca_id = factory.Iterator(CaIdIterator("CSH"))
    ca_hash_id = factory.Faker("uuid4")
    program = factory.SubFactory(RealProgramFactory)
    status_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    status = factory.fuzzy.FuzzyChoice(
        CashPlan.STATUS_CHOICE,
        getter=lambda c: c[0],
    )
    name = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True,
        ext_word_list=None,
    )
    distribution_level = "Registration Group"
    start_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=randint(60, 1000)))
    dispersion_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=randint(60, 1000)))
    coverage_duration = factory.fuzzy.FuzzyInteger(1, 4)
    coverage_unit = factory.Faker(
        "random_element",
        elements=["Day(s)", "Week(s)", "Month(s)", "Year(s)"],
    )
    comments = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True,
        ext_word_list=None,
    )
    delivery_type = factory.fuzzy.FuzzyChoice(
        PaymentRecord.DELIVERY_TYPE_CHOICE,
        getter=lambda c: c[0],
    )
    assistance_measurement = factory.Faker("currency_name")
    assistance_through = factory.LazyAttribute(lambda o: ServiceProvider.objects.order_by("?").first().ca_id)
    vision_id = factory.fuzzy.FuzzyInteger(123534, 12353435234)
    funds_commitment = factory.fuzzy.FuzzyInteger(1000, 99999999)
    exchange_rate = factory.fuzzy.FuzzyDecimal(0.1, 9.9)
    down_payment = factory.fuzzy.FuzzyInteger(1000, 99999999)
    validation_alerts_count = factory.fuzzy.FuzzyInteger(1, 3)
    total_persons_covered = factory.fuzzy.FuzzyInteger(1, 4)
    total_persons_covered_revised = factory.fuzzy.FuzzyInteger(1, 4)

    total_entitled_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_entitled_quantity_revised = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_delivered_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_undelivered_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)

    @factory.post_generation
    def payment_verification_summary(self, create, extracted, **kwargs):
        if not create:
            return

        PaymentVerificationSummaryFactory(payment_plan=self)


class RealPaymentRecordFactory(factory.DjangoModelFactory):
    class Meta:
        model = PaymentRecord

    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    status = factory.fuzzy.FuzzyChoice(
        PaymentRecord.STATUS_CHOICE,
        getter=lambda c: c[0],
    )
    full_name = factory.Faker("name")
    status_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    ca_id = factory.Iterator(CaIdIterator("PR"))
    ca_hash_id = factory.Faker("uuid4")
    household = factory.LazyAttribute(lambda o: Household.objects.order_by("?").first())
    head_of_household = factory.LazyAttribute(lambda o: o.household.head_of_household)
    total_persons_covered = factory.fuzzy.FuzzyInteger(1, 7)
    distribution_modality = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True,
        ext_word_list=None,
    )
    target_population = factory.SubFactory(TargetPopulationFactory)
    entitlement_card_number = factory.Faker("ssn")
    entitlement_card_status = factory.fuzzy.FuzzyChoice(
        PaymentRecord.ENTITLEMENT_CARD_STATUS_CHOICE,
        getter=lambda c: c[0],
    )
    entitlement_card_issue_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    delivery_type = factory.fuzzy.FuzzyChoice(
        PaymentRecord.DELIVERY_TYPE_CHOICE,
        getter=lambda c: c[0],
    )
    currency = factory.Faker("currency_code")
    entitlement_quantity = factory.fuzzy.FuzzyDecimal(100.0, 10000.0)
    delivered_quantity = factory.LazyAttribute(lambda o: Decimal(randint(10, int(o.entitlement_quantity))))
    delivered_quantity_usd = factory.LazyAttribute(lambda o: Decimal(randint(10, int(o.entitlement_quantity))))
    delivery_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    service_provider = factory.LazyAttribute(lambda o: ServiceProvider.objects.order_by("?").first())
    registration_ca_id = factory.Faker("uuid4")


def generate_real_cash_plans():
    if ServiceProvider.objects.count() < 3:
        ServiceProviderFactory.create_batch(3)
    program = RealProgramFactory(status=Program.ACTIVE)
    cash_plans = RealCashPlanFactory.create_batch(3, program=program)
    for cash_plan in cash_plans:
        targeting_criteria = TargetingCriteriaFactory()

        rule = TargetingCriteriaRule.objects.create(targeting_criteria=targeting_criteria)
        TargetingCriteriaRuleFilter.objects.create(
            targeting_criteria_rule=rule, comparison_method="EQUALS", field_name="residence_status", arguments=[REFUGEE]
        )
        target_population = TargetPopulationFactory(
            program=program,
            status=TargetPopulation.STATUS_OPEN,
            targeting_criteria=targeting_criteria,
        )
        target_population.full_rebuild()
        target_population.status = TargetPopulation.STATUS_READY_FOR_CASH_ASSIST
        target_population.save()
        RealPaymentRecordFactory.create_batch(
            5,
            target_population=target_population,
            parent=cash_plan,
        )
    program.households.set(
        PaymentRecord.objects.exclude(status=PaymentRecord.STATUS_ERROR)
        .filter(parent__in=cash_plans)
        .values_list("household__id", flat=True)
    )


def generate_real_cash_plans_for_households(households):
    if ServiceProvider.objects.count() < 3:
        ServiceProviderFactory.create_batch(3, business_area=households[0].business_area)
    program = RealProgramFactory(business_area=households[0].business_area)
    cash_plans = RealCashPlanFactory.create_batch(3, program=program, business_area=households[0].business_area)
    for cash_plan in cash_plans:
        for hh in households:
            RealPaymentRecordFactory(
                parent=cash_plan,
                household=hh,
                business_area=hh.business_area,
            )
    program.households.set(
        PaymentRecord.objects.exclude(status=PaymentRecord.STATUS_ERROR)
        .filter(parent__in=cash_plans)
        .values_list("household__id", flat=True)
    )


def create_payment_verification_plan_with_status(cash_plan, user, business_area, program, target_population, status):
    cash_plan_payment_verification = PaymentVerificationPlanFactory(payment_plan=cash_plan)
    cash_plan_payment_verification.status = status
    cash_plan_payment_verification.save(update_fields=("status",))
    registration_data_import = RegistrationDataImportFactory(imported_by=user, business_area=business_area)
    for _ in range(5):
        household, _ = create_household(
            {
                "registration_data_import": registration_data_import,
                "admin_area": Area.objects.order_by("?").first(),
            },
            {"registration_data_import": registration_data_import},
        )

        household.programs.add(program)

        payment_record = PaymentRecordFactory(
            parent=cash_plan,
            household=household,
            target_population=target_population,
        )

        PaymentVerificationFactory(
            payment_verification_plan=cash_plan_payment_verification,
            payment=payment_record,
            status=PaymentVerification.STATUS_PENDING,
        )
        EntitlementCardFactory(household=household)
    return cash_plan_payment_verification


class PaymentPlanFactory(factory.DjangoModelFactory):
    class Meta:
        model = PaymentPlan

    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    status_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    start_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=randint(60, 1000)))
    exchange_rate = factory.fuzzy.FuzzyDecimal(0.1, 9.9)

    total_entitled_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_entitled_quantity_revised = 0.0
    total_delivered_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_undelivered_quantity = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)

    total_entitled_quantity_usd = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_entitled_quantity_revised_usd = 0.0
    total_delivered_quantity_usd = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)
    total_undelivered_quantity_usd = factory.fuzzy.FuzzyDecimal(20000.0, 90000000.0)

    created_by = factory.SubFactory(UserFactory)
    unicef_id = factory.Faker("uuid4")
    target_population = factory.SubFactory(TargetPopulationFactory)
    program = factory.SubFactory(RealProgramFactory)
    currency = factory.fuzzy.FuzzyChoice(CURRENCY_CHOICES, getter=lambda c: c[0])

    dispersion_start_date = factory.Faker(
        "date_time_this_decade",
        before_now=False,
        after_now=True,
        tzinfo=utc,
    )
    dispersion_end_date = factory.LazyAttribute(lambda o: o.dispersion_start_date + timedelta(days=randint(60, 1000)))
    female_children_count = factory.fuzzy.FuzzyInteger(2, 4)
    male_children_count = factory.fuzzy.FuzzyInteger(2, 4)
    female_adults_count = factory.fuzzy.FuzzyInteger(2, 4)
    male_adults_count = factory.fuzzy.FuzzyInteger(2, 4)
    total_households_count = factory.fuzzy.FuzzyInteger(2, 4)
    total_individuals_count = factory.fuzzy.FuzzyInteger(8, 16)


class PaymentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Payment

    parent = factory.SubFactory(PaymentPlanFactory)
    business_area = factory.LazyAttribute(lambda o: BusinessArea.objects.first())
    status = GenericPayment.STATUS_NOT_DISTRIBUTED
    status_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    household = factory.LazyAttribute(lambda o: HouseholdFactory(head_of_household=IndividualFactory(household=None)))
    head_of_household = factory.LazyAttribute(lambda o: o.household.head_of_household)
    collector = factory.LazyAttribute(
        lambda o: (
            o.household.individuals_and_roles.filter(role=ROLE_PRIMARY).first()
            or IndividualRoleInHouseholdFactory(
                household=o.household, individual=o.household.head_of_household, role=ROLE_PRIMARY
            )
        ).individual
    )
    delivery_type = factory.fuzzy.FuzzyChoice(
        GenericPayment.DELIVERY_TYPE_CHOICE,
        getter=lambda c: c[0],
    )
    currency = factory.Faker("currency_code")
    entitlement_quantity = factory.fuzzy.FuzzyDecimal(100.0, 10000.0)
    entitlement_quantity_usd = factory.LazyAttribute(lambda o: Decimal(randint(10, int(o.entitlement_quantity))))
    delivered_quantity = factory.LazyAttribute(lambda o: Decimal(randint(10, int(o.entitlement_quantity))))
    delivered_quantity_usd = factory.LazyAttribute(lambda o: Decimal(randint(10, int(o.entitlement_quantity))))

    delivery_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    entitlement_date = factory.Faker(
        "date_time_this_decade",
        before_now=False,
        after_now=True,
        tzinfo=utc,
    )
    financial_service_provider = factory.SubFactory(FinancialServiceProviderFactory)
    excluded = False
    assigned_payment_channel = factory.LazyAttribute(lambda o: PaymentChannelFactory(individual=o.collector))


class DeliveryMechanismPerPaymentPlanFactory(factory.DjangoModelFactory):
    class Meta:
        model = DeliveryMechanismPerPaymentPlan

    payment_plan = factory.SubFactory(PaymentPlanFactory)
    financial_service_provider = factory.SubFactory(FinancialServiceProviderFactory)
    created_by = factory.SubFactory(UserFactory)
    sent_by = factory.SubFactory(UserFactory)
    sent_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
        tzinfo=utc,
    )
    delivery_mechanism = factory.fuzzy.FuzzyChoice(
        GenericPayment.DELIVERY_TYPE_CHOICE,
        getter=lambda c: c[0],
    )
    delivery_mechanism_order = factory.fuzzy.FuzzyInteger(1, 4)


def generate_payment_plan():
    # creates a payment plan that has all the necessary data needed to go with it for manual testing

    afghanistan = BusinessArea.objects.get(slug="afghanistan")
    root = User.objects.get(username="root")
    now = timezone.now()
    address = "Ohio"

    rdi_pk = UUID("4d100000-0000-0000-0000-000000000000")
    rdi = RegistrationDataImportFactory(
        pk=rdi_pk,
        name="Test Import",
        number_of_individuals=3,
        number_of_households=1,
        business_area=afghanistan,
    )

    individual_1_pk = UUID("cc000000-0000-0000-0000-000000000001")
    individual_1 = Individual.objects.update_or_create(
        pk=individual_1_pk,
        birth_date=now - timedelta(days=365 * 30),
        first_registration_date=now - timedelta(days=365),
        last_registration_date=now,
        business_area=afghanistan,
        full_name="Jan Kowalski",
        sex=MALE,
    )[0]
    payment_channel_1 = PaymentChannelFactory(
        individual=individual_1,
        delivery_mechanism=Payment.DELIVERY_TYPE_CASH,
    )

    individual_2_pk = UUID("cc000000-0000-0000-0000-000000000002")
    individual_2 = Individual.objects.update_or_create(
        pk=individual_2_pk,
        birth_date=now - timedelta(days=365 * 30),
        first_registration_date=now - timedelta(days=365),
        last_registration_date=now,
        business_area=afghanistan,
        full_name="Adam Nowak",
        sex=MALE,
    )[0]
    payment_channel_2 = PaymentChannelFactory(
        individual=individual_2,
        delivery_mechanism=Payment.DELIVERY_TYPE_CASH,
    )

    household_1_pk = UUID("aa000000-0000-0000-0000-000000000001")
    household_1 = Household.objects.update_or_create(
        pk=household_1_pk,
        size=4,
        head_of_household=individual_1,
        business_area=afghanistan,
        registration_data_import=rdi,
        first_registration_date=now - timedelta(days=365),
        last_registration_date=now,
        address=address,
    )[0]
    individual_1.household = household_1
    individual_1.save()

    household_2_pk = UUID("aa000000-0000-0000-0000-000000000002")
    household_2 = Household.objects.update_or_create(
        pk=household_2_pk,
        size=4,
        head_of_household=individual_2,
        business_area=afghanistan,
        registration_data_import=rdi,
        first_registration_date=now - timedelta(days=365),
        last_registration_date=now,
        address=address,
    )[0]
    individual_2.household = household_2
    individual_2.save()

    program_pk = UUID("00000000-0000-0000-0000-faceb00c0000")
    program = Program.objects.update_or_create(
        pk=program_pk,
        business_area=afghanistan,
        name="Test Program",
        start_date=now,
        end_date=now + timedelta(days=365),
        budget=pow(10, 6),
        cash_plus=True,
        population_goal=250,
        status=Program.ACTIVE,
        frequency_of_payments=Program.ONE_OFF,
        sector=Program.MULTI_PURPOSE,
        scope=Program.SCOPE_UNICEF,
    )[0]

    targeting_criteria_pk = UUID("00000000-0000-0000-0000-feedb00c0000")
    targeting_criteria = TargetingCriteria.objects.update_or_create(
        pk=targeting_criteria_pk,
    )[0]

    targeting_criteria_rule_pk = UUID("00000000-0000-0000-0000-feedb00c0009")
    targeting_criteria_rule = TargetingCriteriaRule.objects.update_or_create(
        pk=targeting_criteria_rule_pk,
        targeting_criteria=targeting_criteria,
    )[0]

    targeting_criteria_rule_condition_pk = UUID("00000000-0000-0000-0000-feedb00c0008")
    TargetingCriteriaRuleFilter.objects.update_or_create(
        pk=targeting_criteria_rule_condition_pk,
        targeting_criteria_rule=targeting_criteria_rule,
        comparison_method="EQUALS",
        field_name="address",
        arguments=[address],
    )

    target_population_pk = UUID("00000000-0000-0000-0000-faceb00c0123")
    target_population = TargetPopulation.objects.update_or_create(
        pk=target_population_pk,
        name="Test Target Population",
        targeting_criteria=targeting_criteria,
        status=TargetPopulation.STATUS_ASSIGNED,
        business_area=afghanistan,
        program=program,
        created_by=root,
    )[0]
    target_population.full_rebuild()
    target_population.save()

    payment_plan_pk = UUID("00000000-feed-beef-0000-00000badf00d")
    payment_plan = PaymentPlan.objects.update_or_create(
        pk=payment_plan_pk,
        business_area=afghanistan,
        target_population=target_population,
        start_date=now,
        end_date=now + timedelta(days=30),
        currency="USD",
        dispersion_start_date=now,
        dispersion_end_date=now + timedelta(days=14),
        status_date=now,
        created_by=root,
        program=program,
    )[0]

    fsp_1_pk = UUID("00000000-0000-0000-0000-f00000000001")
    fsp_1 = FinancialServiceProvider.objects.update_or_create(
        pk=fsp_1_pk,
        name="Test FSP 1",
        delivery_mechanisms=[Payment.DELIVERY_TYPE_CASH],
    )[0]

    payment_1_pk = UUID("10000000-feed-beef-0000-00000badf00d")
    Payment.objects.update_or_create(
        pk=payment_1_pk,
        parent=payment_plan,
        excluded=False,
        business_area=afghanistan,
        household=household_1,
        collector=individual_1,
        delivery_type=Payment.DELIVERY_TYPE_CASH,
        assigned_payment_channel=payment_channel_1,
        financial_service_provider=fsp_1,
        status_date=now,
    )

    payment_2_pk = UUID("20000000-feed-beef-0000-00000badf00d")
    Payment.objects.update_or_create(
        pk=payment_2_pk,
        parent=payment_plan,
        excluded=False,
        business_area=afghanistan,
        household=household_2,
        collector=individual_2,
        delivery_type=Payment.DELIVERY_TYPE_CASH,
        assigned_payment_channel=payment_channel_2,
        financial_service_provider=fsp_1,
        status_date=now,
    )

    payment_plan.update_population_count_fields()
