import json
from decimal import Decimal

from django.db.models import (
    Case,
    CharField,
    Count,
    Exists,
    F,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_relay import to_global_id
from graphql_relay.connection.arrayconnection import connection_from_list_slice

from hct_mis_api.apps.account.permissions import (
    BaseNodePermissionMixin,
    DjangoPermissionFilterConnectionField,
    Permissions,
    hopePermissionClass,
)
from hct_mis_api.apps.activity_log.models import LogEntry
from hct_mis_api.apps.activity_log.schema import LogEntryNode
from hct_mis_api.apps.core.currencies import CURRENCY_CHOICES
from hct_mis_api.apps.core.extended_connection import ExtendedConnection
from hct_mis_api.apps.core.querysets import ExtendedQuerySetSequence
from hct_mis_api.apps.core.schema import ChoiceObject
from hct_mis_api.apps.core.utils import (
    chart_create_filter_query,
    chart_filters_decoder,
    chart_get_filtered_qs,
    chart_map_choices,
    chart_permission_decorator,
    decode_id_string,
    encode_id_base64,
    to_choice_object,
)
from hct_mis_api.apps.geo.models import Area
from hct_mis_api.apps.household.schema import HouseholdNode
from hct_mis_api.apps.payment.filters import (
    FinancialServiceProviderFilter,
    FinancialServiceProviderXlsxReportFilter,
    FinancialServiceProviderXlsxTemplateFilter,
    PaymentFilter,
    PaymentPlanFilter,
    PaymentRecordFilter,
    PaymentVerificationFilter,
    PaymentVerificationLogEntryFilter,
    PaymentVerificationPlanFilter,
)
from hct_mis_api.apps.payment.inputs import GetCashplanVerificationSampleSizeInput
from hct_mis_api.apps.payment.models import (
    Approval,
    ApprovalProcess,
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
from hct_mis_api.apps.payment.services.rapid_pro.api import RapidProAPI
from hct_mis_api.apps.payment.services.sampling import Sampling
from hct_mis_api.apps.payment.tasks.CheckRapidProVerificationTask import (
    does_payment_record_have_right_hoh_phone_number,
)
from hct_mis_api.apps.payment.utils import get_payment_items_for_dashboard
from hct_mis_api.apps.utils.schema import (
    ChartDatasetNode,
    ChartDetailedDatasetsNode,
    SectionTotalNode,
    TableTotalCashTransferred,
)


class RapidProFlowResult(graphene.ObjectType):
    key = graphene.String()
    name = graphene.String()
    categories = graphene.List(graphene.String)
    node_uuids = graphene.List(graphene.String)


class RapidProFlowRun(graphene.ObjectType):
    active = graphene.Int()
    completed = graphene.Int()
    interrupted = graphene.Int()
    expired = graphene.Int()


class RapidProFlow(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    type = graphene.String()
    archived = graphene.Boolean()
    labels = graphene.List(graphene.String)
    expires = graphene.Int()
    runs = graphene.List(RapidProFlowRun)
    results = graphene.List(RapidProFlowResult)
    # parent_refs
    created_on = graphene.DateTime()
    modified_on = graphene.DateTime()

    def resolve_id(parent, info):
        return parent["uuid"]


class FinancialServiceProviderXlsxTemplateNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (
        hopePermissionClass(Permissions.FINANCIAL_SERVICE_PROVIDER_XLSX_TEMPLATE_VIEW_LIST_AND_DETAILS),
    )

    class Meta:
        model = FinancialServiceProviderXlsxTemplate
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class FinancialServiceProviderXlsxReportNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.FINANCIAL_SERVICE_PROVIDER_VIEW_LIST_AND_DETAILS),)

    class Meta:
        model = FinancialServiceProviderXlsxReport
        exclude = ("file",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    report_url = graphene.String()

    def resolve_report_url(self, info, **kwargs):
        return self.file.url if self.file else ""


class FinancialServiceProviderNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.FINANCIAL_SERVICE_PROVIDER_VIEW_LIST_AND_DETAILS),)

    class Meta:
        model = FinancialServiceProvider
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class ServiceProviderNode(DjangoObjectType):
    class Meta:
        model = ServiceProvider
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class AgeFilterObject(graphene.ObjectType):
    min = graphene.Int()
    max = graphene.Int()


class PaymentVerificationSummaryNode(DjangoObjectType):
    class Meta:
        model = PaymentVerificationSummary
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class GetCashplanVerificationSampleSizeObject(graphene.ObjectType):
    payment_record_count = graphene.Int()
    sample_size = graphene.Int()


class ChartPaymentVerification(ChartDetailedDatasetsNode):
    households = graphene.Int()
    average_sample_size = graphene.Float()


class ApprovalNode(DjangoObjectType):
    info = graphene.String()

    class Meta:
        model = Approval
        fields = ("created_at", "comment", "info", "created_by")

    def resolve_info(self, info):
        return self.info


class FilteredActionsListNode(graphene.ObjectType):
    approval = graphene.List(ApprovalNode)
    authorization = graphene.List(ApprovalNode)
    finance_review = graphene.List(ApprovalNode)
    reject = graphene.List(ApprovalNode)


class ApprovalProcessNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.PAYMENT_MODULE_VIEW_DETAILS),)
    rejected_on = graphene.String()
    actions = graphene.Field(FilteredActionsListNode)

    class Meta:
        model = ApprovalProcess
        exclude = ("approvals",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_rejected_on(self, info):
        if self.approvals.filter(type=Approval.REJECT).exists():
            if self.sent_for_finance_review_date:
                return "IN_REVIEW"
            if self.sent_for_authorization_date:
                return "IN_AUTHORIZATION"
            if self.sent_for_approval_date:
                return "IN_APPROVAL"
        return None

    def resolve_actions(self, info):
        resp = FilteredActionsListNode(
            approval=self.approvals.filter(type=Approval.APPROVAL),
            authorization=self.approvals.filter(type=Approval.AUTHORIZATION),
            finance_review=self.approvals.filter(type=Approval.FINANCE_REVIEW),
            reject=self.approvals.filter(type=Approval.REJECT),
        )
        return resp


class PaymentConflictDataNode(graphene.ObjectType):
    payment_plan_id = graphene.String()
    payment_plan_unicef_id = graphene.String()
    payment_plan_start_date = graphene.String()
    payment_plan_end_date = graphene.String()
    payment_plan_status = graphene.String()
    payment_id = graphene.String()
    payment_unicef_id = graphene.String()

    def resolve_payment_plan_id(self, info):
        return encode_id_base64(self["payment_plan_id"], "PaymentPlan")

    def resolve_payment_id(self, info):
        return encode_id_base64(self["payment_id"], "Payment")


class GenericPaymentNode(graphene.ObjectType):
    """using this for GenericFK like in PaymentVerification (Payment and PaymentRecord models)"""

    id = graphene.String()
    obj_type = graphene.String()
    unicef_id = graphene.String()
    currency = graphene.String()
    delivered_quantity = graphene.Float()
    delivered_quantity_usd = graphene.Float()
    household = graphene.Field(HouseholdNode)

    def resolve_id(self, info):
        return to_global_id(self.__class__.__name__ + "Node", self.id)

    def resolve_obj_type(self, info):
        return self.__class__.__name__

    def resolve_unicef_id(self, info):
        return self.unicef_id

    def resolve_currency(self, info):
        return self.currency

    def resolve_delivered_quantity_usd(self, info):
        return self.delivered_quantity_usd

    def resolve_delivered_quantity(self, info):
        return self.delivered_quantity

    def resolve_household(self, info):
        return self.household


class PaymentNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.PAYMENT_MODULE_VIEW_DETAILS),)
    payment_plan_hard_conflicted = graphene.Boolean()
    payment_plan_hard_conflicted_data = graphene.List(PaymentConflictDataNode)
    payment_plan_soft_conflicted = graphene.Boolean()
    payment_plan_soft_conflicted_data = graphene.List(PaymentConflictDataNode)
    has_payment_channel = graphene.Boolean()

    class Meta:
        model = Payment
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_payment_plan_hard_conflicted_data(self, info) -> list:
        if self.parent.status != PaymentPlan.Status.OPEN:
            return list()
        return PaymentNode._parse_pp_conflict_data(getattr(self, "payment_plan_hard_conflicted_data", []))

    def resolve_payment_plan_soft_conflicted_data(self, info) -> list:
        if self.parent.status != PaymentPlan.Status.OPEN:
            return list()
        return PaymentNode._parse_pp_conflict_data(getattr(self, "payment_plan_soft_conflicted_data", []))

    def resolve_has_payment_channel(self, info) -> bool:
        return self.collector.payment_channels.exists()

    def resolve_payment_plan_hard_conflicted(self, info) -> bool:
        return self.parent.status == PaymentPlan.Status.OPEN and self.payment_plan_hard_conflicted

    def resolve_payment_plan_soft_conflicted(self, info) -> bool:
        return self.parent.status == PaymentPlan.Status.OPEN and self.payment_plan_soft_conflicted

    @classmethod
    def _parse_pp_conflict_data(cls, conflicts_data):
        """parse list of conflicted payment plans data from Payment model json annotations"""
        return [json.loads(conflict) for conflict in conflicts_data]


class DeliveryMechanismNode(DjangoObjectType):
    name = graphene.String()
    order = graphene.Int()
    fsp = graphene.Field(FinancialServiceProviderNode)

    def resolve_name(self, info):
        return self.delivery_mechanism

    def resolve_order(self, info):
        return self.delivery_mechanism_order

    def resolve_fsp(self, info):
        return self.financial_service_provider

    class Meta:
        model = DeliveryMechanismPerPaymentPlan
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


def _calculate_volume(delivery_mechanism_per_payment_plan, field):
    if not delivery_mechanism_per_payment_plan.financial_service_provider:
        return None
    payments = delivery_mechanism_per_payment_plan.payment_plan.not_excluded_payments.filter(
        financial_service_provider=delivery_mechanism_per_payment_plan.financial_service_provider,
        assigned_payment_channel__delivery_mechanism=delivery_mechanism_per_payment_plan.delivery_mechanism,
    )
    return payments.aggregate(entitlement_sum=Coalesce(Sum(field), Decimal(0.0)))["entitlement_sum"]


class VolumeByDeliveryMechanismNode(graphene.ObjectType):
    delivery_mechanism = graphene.Field(DeliveryMechanismNode)
    volume = graphene.Float()
    volume_usd = graphene.Float()

    def resolve_delivery_mechanism(self, info):
        return self  # DeliveryMechanismNode uses the same model

    def resolve_volume(self, info):  # non-usd
        return _calculate_volume(self, "entitlement_quantity")

    def resolve_volume_usd(self, info):
        return _calculate_volume(self, "entitlement_quantity_usd")

    class Meta:
        model = DeliveryMechanismPerPaymentPlan
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class FspChoices(graphene.ObjectType):
    class FspChoice(graphene.ObjectType):
        id = graphene.String()
        name = graphene.String()

        def resolve_id(self, info):
            return encode_id_base64(self["id"], "FinancialServiceProvider")

    delivery_mechanism = graphene.String()
    fsps = graphene.List(FspChoice)


class PaymentPlanNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.PAYMENT_MODULE_VIEW_DETAILS),)
    approval_number_required = graphene.Int()
    authorization_number_required = graphene.Int()
    finance_review_number_required = graphene.Int()
    dispersion_start_date = graphene.Date()
    dispersion_end_date = graphene.Date()
    start_date = graphene.Date()
    end_date = graphene.Date()
    currency_name = graphene.String()
    has_payment_list_export_file = graphene.Boolean()
    imported_file_name = graphene.String()
    payments_conflicts_count = graphene.Int()
    delivery_mechanisms = graphene.List(DeliveryMechanismNode)
    volume_by_delivery_mechanism = graphene.List(VolumeByDeliveryMechanismNode)

    class Meta:
        model = PaymentPlan
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_approval_number_required(self, info):
        return self.business_area.approval_number_required

    def resolve_authorization_number_required(self, info):
        return self.business_area.authorization_number_required

    def resolve_finance_review_number_required(self, info):
        return self.business_area.finance_review_number_required

    def resolve_payments_conflicts_count(self, info):
        return self.payment_items.filter(payment_plan_hard_conflicted=True).count()

    def resolve_currency_name(self, info):
        return self.get_currency_display()

    def resolve_delivery_mechanisms(self, info):
        return DeliveryMechanismPerPaymentPlan.objects.filter(payment_plan=self).order_by("delivery_mechanism_order")

    def resolve_has_payment_list_export_file(self, info):
        return self.has_export_file

    def resolve_imported_file_name(self, info):
        return self.imported_file.file.name if self.imported_file else ""

    def resolve_volume_by_delivery_mechanism(self, info):
        return DeliveryMechanismPerPaymentPlan.objects.filter(payment_plan=self).order_by("delivery_mechanism_order")


class PaymentVerificationNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.PAYMENT_VERIFICATION_VIEW_PAYMENT_RECORD_DETAILS),)
    is_manually_editable = graphene.Boolean()
    payment = graphene.Field(GenericPaymentNode)

    class Meta:
        model = PaymentVerification
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_payment(self, info):
        return self.payment


class PaymentVerificationPlanNode(DjangoObjectType):
    excluded_admin_areas_filter = graphene.List(graphene.String)
    age_filter = graphene.Field(AgeFilterObject)
    xlsx_file_was_downloaded = graphene.Boolean()
    has_xlsx_file = graphene.Boolean()
    payment_plan = graphene.Field(PaymentPlanNode)

    class Meta:
        model = PaymentVerificationPlan
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_xlsx_file_was_downloaded(self, info):
        return self.xlsx_payment_verification_plan_file_was_downloaded

    def resolve_has_xlsx_file(self, info):
        return self.has_xlsx_payment_verification_plan_file


class PaymentRecordNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.PROGRAMME_VIEW_PAYMENT_RECORD_DETAILS),)
    verification = graphene.Field(PaymentVerificationNode)

    class Meta:
        model = PaymentRecord
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class PaymentVerificationLogEntryNode(LogEntryNode):
    content_object = graphene.Field(PaymentVerificationPlanNode)

    class Meta:
        model = LogEntry
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class PaymentChannelNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (hopePermissionClass(Permissions.PAYMENT_MODULE_VIEW_DETAILS),)

    class Meta:
        model = PaymentChannel
        exclude = ("delivery_data",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class AvailableFspsForDeliveryMechanismsInput(graphene.InputObjectType):
    payment_plan_id = graphene.ID(required=True)


class CashPlanAndPaymentPlanNode(BaseNodePermissionMixin, graphene.ObjectType):
    """
    for CashPlan and PaymentPlan models
    """

    permission_classes = (
        hopePermissionClass(Permissions.PAYMENT_VERIFICATION_VIEW_DETAILS),
        hopePermissionClass(Permissions.PRORGRAMME_VIEW_LIST_AND_DETAILS),
    )

    obj_type = graphene.String()
    id = graphene.String()
    unicef_id = graphene.String()
    verification_status = graphene.String()
    currency = graphene.String()
    total_delivered_quantity = graphene.Float()
    start_date = graphene.String()
    end_date = graphene.String()
    programme_name = graphene.String()
    updated_at = graphene.String()
    verification_plans = graphene.List(PaymentVerificationPlanNode)
    total_number_of_households = graphene.Int()
    total_entitled_quantity = graphene.Float()
    total_undelivered_quantity = graphene.Float()

    # TODO: Fields with dummy data
    assistance_measurement = graphene.String()
    dispersion_date = graphene.String()
    service_provider_full_name = graphene.String()

    def resolve_id(self, info, **kwargs):
        return to_global_id(self.__class__.__name__ + "Node", self.id)

    def resolve_obj_type(self, info, **kwargs):
        return self.__class__.__name__

    def resolve_verification_status(self, info, **kwargs):
        return self.payment_verification_summary.status if self.payment_verification_summary else None

    def resolve_programme_name(self, info, **kwargs):
        return self.program.name

    def resolve_verification_plans(self, info, **kwargs):
        return self.payment_verification_plans.all()

    def resolve_assistance_measurement(self, info, **kwargs):
        return "HH"

    def resolve_dispersion_date(self, info, **kwargs):
        return ""

    def resolve_service_provider_full_name(self, info, **kwargs):
        return ""


class PageInfoNode(graphene.ObjectType):
    start_cursor = graphene.String()
    end_cursor = graphene.String()
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()


class CashPlanAndPaymentPlanEdges(graphene.ObjectType):
    cursor = graphene.String()
    node = graphene.Field(CashPlanAndPaymentPlanNode)


class PaginatedCashPlanAndPaymentPlanNode(graphene.ObjectType):
    page_info = graphene.Field(PageInfoNode)
    edges = graphene.List(CashPlanAndPaymentPlanEdges)
    total_count = graphene.Int()


class GenericPaymentPlanNode(graphene.ObjectType):
    # TODO: add perms
    # permission_classes = (
    #     hopePermissionClass(Permissions.PAYMENT_VERIFICATION_VIEW_DETAILS),
    #     hopePermissionClass(Permissions.PRORGRAMME_VIEW_LIST_AND_DETAILS),
    # )

    id = graphene.String()
    obj_type = graphene.String()
    payment_verification_summary = graphene.Field(PaymentVerificationSummaryNode)

    def resolve_id(self, info, **kwargs):
        return to_global_id(self.__class__.__name__ + "Node", self.id)

    def resolve_obj_type(self, info, **kwargs):
        return self.__class__.__name__

    def resolve_payment_verification_summary(
        self,
        info,
    ):
        return self.payment_verification_summary


class CashPlanOrPaymentPlanNode(BaseNodePermissionMixin, graphene.ObjectType):
    permission_classes = (
        hopePermissionClass(Permissions.PAYMENT_VERIFICATION_VIEW_DETAILS),
        hopePermissionClass(Permissions.PRORGRAMME_VIEW_LIST_AND_DETAILS),
    )

    id = graphene.ID()
    can_create_payment_verification_plan = graphene.Boolean()
    available_payment_records_count = graphene.Int()
    start_date = graphene.Date()
    end_date = graphene.Date()
    updated_at = graphene.DateTime()
    status = graphene.String()
    delivery_type = graphene.String()
    program = graphene.Field("hct_mis_api.apps.program.schema.ProgramNode")
    payment_items = graphene.List(PaymentNode, required=False)
    # payment_record_items = graphene.List(PaymentRecordNode, source="payment_items")
    # payment_items = DjangoPermissionFilterConnectionField(
    #     PaymentNode,
    #     filterset_class=PaymentFilter,
    # )
    payment_record_items = DjangoPermissionFilterConnectionField(
        PaymentRecordNode,
        source="payment_items",
        filterset_class=PaymentRecordFilter,
    )

    unicef_id = graphene.String()
    bank_reconciliation_success = graphene.Int()
    bank_reconciliation_error = graphene.Int()
    delivery_type = graphene.String()
    total_number_of_households = graphene.Int()
    currency = graphene.String(source="currency")
    total_delivered_quantity = graphene.Float()
    total_entitled_quantity = graphene.Float()
    total_undelivered_quantity = graphene.Float()
    verification_plans = DjangoPermissionFilterConnectionField(
        "hct_mis_api.apps.payment.schema.PaymentVerificationPlanNode",
        source="payment_verification_plans",
        filterset_class=PaymentVerificationPlanFilter,
    )
    payment_verification_summary = graphene.Field(PaymentVerificationSummaryNode)

    # TODO: Think what to do to make it compatible with CashPlanNode
    # Added these fields to for compatibility with CashPlanNode
    name = graphene.String()
    funds_commitment = graphene.String()
    down_payment = graphene.String()
    dispersion_date = graphene.String()
    assistance_through = graphene.String()
    service_provider = graphene.Field(ServiceProviderNode)
    ca_id = graphene.String()
    ca_hash_id = graphene.String()

    def resolve_id(self, info, **kwargs):
        return to_global_id(self.__class__.__name__ + "Node", self.id)

    def resolve_unicef_id(self, info):
        return getattr(self, "unicef_id", None)

    def resolve_total_number_of_households(self, info, **kwargs):
        return getattr(self, "total_households_count", None)

    def resolve_can_create_payment_verification_plan(self, info, **kwargs):
        return getattr(self, "can_create_payment_verification_plan", False)

    def resolve_available_payment_records_count(self, info, **kwargs):
        return self.payment_items.filter(
            status__in=PaymentRecord.ALLOW_CREATE_VERIFICATION, delivered_quantity__gt=0
        ).count()

    def resolve_name(self, info):
        return getattr(self, "name", None)

    def resolve_funds_commitment(self, info):
        return getattr(self, "funds_commitment", None)

    def resolve_down_payment(self, info):
        return getattr(self, "down_payment", None)

    def resolve_dispersion_date(self, info):
        return getattr(self, "dispersion_date", None)

    def resolve_assistance_through(self, info):
        return getattr(self, "assistance_through", None)

    def resolve_service_provider(self, info):
        return getattr(self, "service_provider", None)

    def resolve_ca_id(self, info):
        return getattr(self, "ca_id", None)

    def resolve_ca_hash_id(self, info):
        return getattr(self, "ca_hash_id", None)

    def resolve_payment_items(self, info, **kwargs):
        if self.payment_items.count() > 0:
            return self.payment_items.all()
        return []


class Query(graphene.ObjectType):
    payment_record = relay.Node.Field(PaymentRecordNode)
    financial_service_provider_xlsx_template = relay.Node.Field(FinancialServiceProviderXlsxTemplateNode)
    all_financial_service_provider_xlsx_templates = DjangoPermissionFilterConnectionField(
        FinancialServiceProviderXlsxTemplateNode,
        filterset_class=FinancialServiceProviderXlsxTemplateFilter,
    )
    financial_service_provider_xlsx_report = relay.Node.Field(FinancialServiceProviderXlsxReportNode)
    all_financial_service_provider_xlsx_reports = DjangoPermissionFilterConnectionField(
        FinancialServiceProviderXlsxReportNode,
        filterset_class=FinancialServiceProviderXlsxReportFilter,
    )
    financial_service_provider = relay.Node.Field(FinancialServiceProviderNode)
    all_financial_service_providers = DjangoPermissionFilterConnectionField(
        FinancialServiceProviderNode,
        filterset_class=FinancialServiceProviderFilter,
    )
    payment_record_verification = relay.Node.Field(PaymentVerificationNode)
    payment_verification_plan = relay.Node.Field(PaymentVerificationPlanNode)
    all_payment_records = DjangoPermissionFilterConnectionField(
        PaymentRecordNode,
        filterset_class=PaymentRecordFilter,
        permission_classes=(hopePermissionClass(Permissions.PRORGRAMME_VIEW_LIST_AND_DETAILS),),
    )
    all_payment_verifications = DjangoPermissionFilterConnectionField(
        PaymentVerificationNode,
        filterset_class=PaymentVerificationFilter,
        # permission_classes=(hopePermissionClass(Permissions.PAYMENT_VERIFICATION_VIEW_DETAILS),),  # TODO check perms
    )
    all_payment_verification_plan = DjangoPermissionFilterConnectionField(
        PaymentVerificationPlanNode,
        filterset_class=PaymentVerificationPlanFilter,
        permission_classes=(hopePermissionClass(Permissions.PAYMENT_VERIFICATION_VIEW_DETAILS),),
    )

    chart_payment_verification = graphene.Field(
        ChartPaymentVerification,
        business_area_slug=graphene.String(required=True),
        year=graphene.Int(required=True),
        program=graphene.String(required=False),
        administrative_area=graphene.String(required=False),
    )
    chart_volume_by_delivery_mechanism = graphene.Field(
        ChartDatasetNode,
        business_area_slug=graphene.String(required=True),
        year=graphene.Int(required=True),
        program=graphene.String(required=False),
        administrative_area=graphene.String(required=False),
    )
    chart_payment = graphene.Field(
        ChartDatasetNode,
        business_area_slug=graphene.String(required=True),
        year=graphene.Int(required=True),
        program=graphene.String(required=False),
        administrative_area=graphene.String(required=False),
    )
    section_total_transferred = graphene.Field(
        SectionTotalNode,
        business_area_slug=graphene.String(required=True),
        year=graphene.Int(required=True),
        program=graphene.String(required=False),
        administrative_area=graphene.String(required=False),
    )
    table_total_cash_transferred_by_administrative_area = graphene.Field(
        TableTotalCashTransferred,
        business_area_slug=graphene.String(required=True),
        year=graphene.Int(required=True),
        program=graphene.String(required=False),
        administrative_area=graphene.String(required=False),
        order=graphene.String(required=False),
        order_by=graphene.String(required=False),
    )
    chart_total_transferred_cash_by_country = graphene.Field(
        ChartDetailedDatasetsNode, year=graphene.Int(required=True)
    )

    payment_record_status_choices = graphene.List(ChoiceObject)
    payment_record_entitlement_card_status_choices = graphene.List(ChoiceObject)
    payment_record_delivery_type_choices = graphene.List(ChoiceObject)
    cash_plan_verification_status_choices = graphene.List(ChoiceObject)
    cash_plan_verification_sampling_choices = graphene.List(ChoiceObject)
    cash_plan_verification_verification_channel_choices = graphene.List(ChoiceObject)
    payment_verification_status_choices = graphene.List(ChoiceObject)

    all_rapid_pro_flows = graphene.List(
        RapidProFlow,
        business_area_slug=graphene.String(required=True),
    )
    sample_size = graphene.Field(
        GetCashplanVerificationSampleSizeObject,
        input=GetCashplanVerificationSampleSizeInput(),
    )

    all_payment_verification_log_entries = DjangoPermissionFilterConnectionField(
        PaymentVerificationLogEntryNode,
        filterset_class=PaymentVerificationLogEntryFilter,
        permission_classes=(hopePermissionClass(Permissions.ACTIVITY_LOG_VIEW),),
    )

    payment_plan = relay.Node.Field(PaymentPlanNode)
    # TODO: Keep or remove??? in favour of all_cash_plans_and_payment_plans
    all_payment_plans = DjangoPermissionFilterConnectionField(
        PaymentPlanNode,
        filterset_class=PaymentPlanFilter,
        permission_classes=(hopePermissionClass(Permissions.PAYMENT_MODULE_VIEW_LIST),),
    )
    payment_plan_status_choices = graphene.List(ChoiceObject)
    currency_choices = graphene.List(ChoiceObject)
    payment = relay.Node.Field(PaymentNode)
    all_payments = DjangoPermissionFilterConnectionField(
        PaymentNode,
        filterset_class=PaymentFilter,
        permission_classes=(hopePermissionClass(Permissions.PAYMENT_MODULE_VIEW_LIST),),
    )
    all_delivery_mechanisms = graphene.List(ChoiceObject)
    payment_plan_background_action_status_choices = graphene.List(ChoiceObject)
    available_fsps_for_delivery_mechanisms = graphene.List(
        FspChoices,
        input=AvailableFspsForDeliveryMechanismsInput(),
    )
    cash_plan_or_payment_plan = graphene.Field(
        CashPlanOrPaymentPlanNode,
        description="Get a cash plan or payment plan by id",
        id=graphene.ID(required=True),
        plan_type=graphene.String(required=True),
    )
    all_cash_plans_and_payment_plans = graphene.Field(
        PaginatedCashPlanAndPaymentPlanNode,
        business_area=graphene.String(required=True),
        program=graphene.String(),
        search=graphene.String(),
        service_provider=graphene.String(),
        delivery_type=graphene.String(),
        verification_status=graphene.String(),
        start_date_gte=graphene.String(),
        end_date_lte=graphene.String(),
        order_by=graphene.String(),
        first=graphene.Int(),
        last=graphene.Int(),
        before=graphene.String(),
        after=graphene.String(),
    )

    def resolve_cash_plan_or_payment_plan(self, info, id, plan_type, **kwargs):
        if plan_type == "CashPlan":
            data = CashPlan.objects.get(id=decode_id_string(id))
        elif plan_type == "PaymentPlan":
            data = PaymentPlan.objects.get(id=decode_id_string(id))
        else:
            raise Exception("Invalid plan type")

        return data

    def resolve_available_fsps_for_delivery_mechanisms(self, info, input, **kwargs):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(input["payment_plan_id"]))
        delivery_mechanisms = (
            DeliveryMechanismPerPaymentPlan.objects.filter(payment_plan=payment_plan)
            .values_list("delivery_mechanism", flat=True)
            .order_by("delivery_mechanism_order")
        )

        def get_fsps_for_delivery_mechanism(mechanism):
            fsps = FinancialServiceProvider.objects.filter(delivery_mechanisms__contains=[mechanism]).distinct()
            return (
                [
                    # This basically checks if FSP can accept ANY additional volume,
                    # more strict validation is performed in AssignFspToDeliveryMechanismMutation
                    {"id": fsp.id, "name": fsp.name}
                    for fsp in fsps
                    if fsp.can_accept_any_volume()
                ]
                if fsps
                else []
            )

        return [
            {"delivery_mechanism": mechanism, "fsps": get_fsps_for_delivery_mechanism(mechanism)}
            for mechanism in delivery_mechanisms
        ]

    def resolve_all_payment_verifications(self, info, **kwargs):
        # TODO: FIX error
        # "'ExtendedQuerySetSequence' object has no attribute 'clone'"
        # payment_qs = get_payment_items_sequence_qs().filter(id=OuterRef("payment_object_id"))
        # payment_qs = Payment.objects.filter(id=OuterRef("payment_object_id"), household__withdrawn=True)

        return (
            PaymentVerification.objects.filter(
                Q(payment_verification_plan__status=PaymentVerificationPlan.STATUS_ACTIVE)
                | Q(payment_verification_plan__status=PaymentVerificationPlan.STATUS_FINISHED)
            )
            # .annotate(
            #     payment__household__status=Case(
            #         When(Exists(payment_qs), then=Value(STATUS_INACTIVE)),
            #         default=Value(STATUS_ACTIVE),
            #         output_field=CharField(),
            #     ),
            # )
            .distinct()
        )

    def resolve_sample_size(self, info, input, **kwargs):
        def get_payment_records(cash_plan, payment_verification_plan, verification_channel):
            kwargs = {}
            if payment_verification_plan:
                kwargs["payment_verification_plan"] = payment_verification_plan
            if verification_channel == PaymentVerificationPlan.VERIFICATION_CHANNEL_RAPIDPRO:
                kwargs["extra_validation"] = does_payment_record_have_right_hoh_phone_number
            return cash_plan.available_payment_records(**kwargs)

        cash_plan_id = decode_id_string(input.get("cash_plan_id"))
        cash_plan = get_object_or_404(CashPlan, id=cash_plan_id)

        payment_verification_plan = None
        if payment_verification_plan_id := decode_id_string(input.get("cash_plan_payment_verification_id")):
            payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=payment_verification_plan_id)

        payment_records = get_payment_records(cash_plan, payment_verification_plan, input.get("verification_channel"))
        if not payment_records:
            return {
                "sample_size": 0,
                "payment_record_count": 0,
            }

        sampling = Sampling(input, cash_plan, payment_records)
        payment_record_count, payment_records_sample_count = sampling.generate_sampling()

        return {
            "payment_record_count": payment_record_count,
            "sample_size": payment_records_sample_count,
        }

    def resolve_all_rapid_pro_flows(self, info, business_area_slug, **kwargs):
        api = RapidProAPI(business_area_slug)
        return api.get_flows()

    def resolve_payment_record_status_choices(self, info, **kwargs):
        return to_choice_object(PaymentRecord.STATUS_CHOICE)

    def resolve_payment_record_entitlement_card_status_choices(self, info, **kwargs):
        return to_choice_object(PaymentRecord.ENTITLEMENT_CARD_STATUS_CHOICE)

    def resolve_payment_record_delivery_type_choices(self, info, **kwargs):
        return to_choice_object(PaymentRecord.DELIVERY_TYPE_CHOICE)

    def resolve_cash_plan_verification_status_choices(self, info, **kwargs):
        return to_choice_object(PaymentVerificationPlan.STATUS_CHOICES)

    def resolve_cash_plan_verification_sampling_choices(self, info, **kwargs):
        return to_choice_object(PaymentVerificationPlan.SAMPLING_CHOICES)

    def resolve_cash_plan_verification_verification_channel_choices(self, info, **kwargs):
        return to_choice_object(PaymentVerificationPlan.VERIFICATION_CHANNEL_CHOICES)

    def resolve_payment_verification_status_choices(self, info, **kwargs):
        return to_choice_object(PaymentVerification.STATUS_CHOICES)

    def resolve_all_delivery_mechanisms(self, info, **kwargs):
        return to_choice_object(GenericPayment.DELIVERY_TYPE_CHOICE)

    @chart_permission_decorator(permissions=[Permissions.DASHBOARD_VIEW_COUNTRY])
    def resolve_chart_payment_verification(self, info, business_area_slug, year, **kwargs):
        filters = chart_filters_decoder(kwargs)
        status_choices_mapping = chart_map_choices(PaymentVerification.STATUS_CHOICES)
        additional_filters = (
            chart_create_filter_query(
                filters,
                program_id_path="payment__parent__program__id,payment_record__parent__program__id",
                administrative_area_path="payment__household__admin_area,payment_record__parent__program__id",
                payment_verification_gfk=True,
            )
        )
        payment_verifications = chart_get_filtered_qs(
            PaymentVerification.objects,
            year,
            business_area_slug_filter={
                "payment__business_area__slug": business_area_slug,
                "payment_record__business_area__slug": business_area_slug,
            },
            additional_filters=additional_filters if isinstance(additional_filters, Q) else {**additional_filters},
            year_filter_path="payment__delivery_date,payment_record__delivery_date",
            payment_verification_gfk=True,
        )

        verifications_by_status = payment_verifications.values("status").annotate(count=Count("status"))
        verifications_by_status_dict = {x.get("status"): x.get("count") for x in verifications_by_status}
        dataset = [verifications_by_status_dict.get(status, 0) for status in status_choices_mapping.keys()]
        try:
            all_verifications = sum(dataset)
            dataset_percentage = [data / all_verifications for data in dataset]
        except ZeroDivisionError:
            dataset_percentage = [0] * len(status_choices_mapping.values())
        dataset_percentage_done = [
            {"label": status, "data": [dataset_percentage_value]}
            for (dataset_percentage_value, status) in zip(dataset_percentage, status_choices_mapping.values())
        ]

        samples_count = payment_verifications.distinct("payment").count()
        all_payment_records_for_created_verifications = (
            PaymentRecord.objects.filter(
                parent__in=payment_verifications.distinct("payment_verification_plan__payment_plan").values_list(
                    "payment_verification_plan__payment_plan", flat=True
                )
            )
            .filter(status=PaymentRecord.STATUS_SUCCESS, delivered_quantity__gt=0)
            .count()
        )
        if samples_count == 0 or all_payment_records_for_created_verifications == 0:
            average_sample_size = 0
        else:
            average_sample_size = samples_count / all_payment_records_for_created_verifications
        return {
            "labels": ["Payment Verification"],
            "datasets": dataset_percentage_done,
            "households": payment_verifications.distinct("payment__household").count(),
            "average_sample_size": average_sample_size,
        }

    @chart_permission_decorator(permissions=[Permissions.DASHBOARD_VIEW_COUNTRY])
    def resolve_chart_volume_by_delivery_mechanism(self, info, business_area_slug, year, **kwargs):
        payment_items_qs: ExtendedQuerySetSequence = get_payment_items_for_dashboard(
            year, business_area_slug, chart_filters_decoder(kwargs), True
        )

        volume_by_delivery_type = (
            payment_items_qs.values("delivery_type")
            .order_by("delivery_type")
            .annotate(volume=Sum("delivered_quantity_usd"))
            .merge_by(
                "delivery_type",
                aggregated_fields=["volume"],
            )
        )

        labels = []
        data = []
        for volume_dict in volume_by_delivery_type:
            if volume_dict.get("volume"):
                labels.append(volume_dict.get("delivery_type"))
                data.append(volume_dict.get("volume"))

        return {"labels": labels, "datasets": [{"data": data}]}

    @chart_permission_decorator(permissions=[Permissions.DASHBOARD_VIEW_COUNTRY])
    def resolve_chart_payment(self, info, business_area_slug, year, **kwargs):
        payment_items_qs: ExtendedQuerySetSequence = get_payment_items_for_dashboard(
            year, business_area_slug, chart_filters_decoder(kwargs)
        )
        payment_items_dict = payment_items_qs.aggregate(
            successful=Count("id", filter=~Q(status=GenericPayment.STATUS_ERROR)),
            unsuccessful=Count("id", filter=Q(status=GenericPayment.STATUS_ERROR)),
        )

        dataset = [
            {
                "data": [
                    payment_items_dict.get("successful", 0),
                    payment_items_dict.get("unsuccessful", 0),
                ]
            }
        ]

        return {"labels": ["Successful Payments", "Unsuccessful Payments"], "datasets": dataset}

    @chart_permission_decorator(permissions=[Permissions.DASHBOARD_VIEW_COUNTRY])
    def resolve_section_total_transferred(self, info, business_area_slug, year, **kwargs):
        payment_items_qs: ExtendedQuerySetSequence = get_payment_items_for_dashboard(
            year, business_area_slug, chart_filters_decoder(kwargs)
        )
        return {"total": payment_items_qs.aggregate(Sum("delivered_quantity_usd"))["delivered_quantity_usd__sum"]}

    @chart_permission_decorator(permissions=[Permissions.DASHBOARD_VIEW_COUNTRY])
    def resolve_table_total_cash_transferred_by_administrative_area(self, info, business_area_slug, year, **kwargs):
        if business_area_slug == "global":
            return None
        order = kwargs.pop("order", None)
        order_by = kwargs.pop("order_by", None)
        payment_items_ids = get_payment_items_for_dashboard(
            year, business_area_slug, chart_filters_decoder(kwargs), True
        ).values_list("id", flat=True)

        admin_areas = (
            Area.objects.filter(
                Q(household__paymentrecord__id__in=payment_items_ids) | Q(household__payment__id__in=payment_items_ids),
                area_type__area_level=2,
            )
            .distinct()
            .annotate(
                total_transferred_payment_records=Sum("household__paymentrecord__delivered_quantity_usd"),
                total_transferred_payments=Sum("household__payment__delivered_quantity_usd"),
            )
            .annotate(
                num_households=Count("household", distinct=True),
                total_transferred=F("total_transferred_payments") + F("total_transferred_payment_records"),
            )
        )

        if order_by:
            order_by_arg = None
            if order_by == "admin2":
                order_by_arg = "name"
            elif order_by == "totalCashTransferred":
                order_by_arg = "total_transferred"
            elif order_by == "totalHouseholds":
                order_by_arg = "num_households"
            if order_by_arg:
                admin_areas = admin_areas.order_by(f"{'-' if order == 'desc' else ''}{order_by_arg}")

        data = [
            {
                "id": item.id,
                "admin2": item.name,
                "total_cash_transferred": item.total_transferred,
                "total_households": item.num_households,
            }
            for item in admin_areas
        ]

        return {"data": data}

    @chart_permission_decorator(permissions=[Permissions.DASHBOARD_VIEW_COUNTRY])
    def resolve_chart_total_transferred_cash_by_country(self, info, year, **kwargs):
        payment_items_qs: ExtendedQuerySetSequence = get_payment_items_for_dashboard(year, "global", {}, True)

        countries_and_amounts: dict = (
            payment_items_qs.select_related("business_area")
            .values("business_area")
            .order_by("business_area")
            .annotate(
                total_delivered_cash=Sum(
                    "delivered_quantity_usd", filter=Q(delivery_type__in=GenericPayment.DELIVERY_TYPES_IN_CASH)
                ),
                total_delivered_voucher=Sum(
                    "delivered_quantity_usd", filter=Q(delivery_type__in=GenericPayment.DELIVERY_TYPES_IN_VOUCHER)
                ),
                business_area_name=F("business_area__name"),
            )
            .order_by("business_area_name")
            .merge_by("business_area_name", aggregated_fields=["total_delivered_cash", "total_delivered_voucher"])
        )

        labels = []
        cash_transferred = []
        voucher_transferred = []
        total_transferred = []
        for data_dict in countries_and_amounts:
            labels.append(data_dict.get("business_area_name"))
            cash_transferred.append(data_dict.get("total_delivered_cash") or 0)
            voucher_transferred.append(data_dict.get("total_delivered_voucher") or 0)
            total_transferred.append(cash_transferred[-1] + voucher_transferred[-1])

        datasets = [
            {"label": "Actual cash transferred", "data": cash_transferred},
            {"label": "Actual voucher transferred", "data": voucher_transferred},
            {"label": "Total transferred", "data": total_transferred},
        ]

        return {"labels": labels, "datasets": datasets}

    def resolve_currency_choices(self, *args, **kwargs):
        return to_choice_object([c for c in CURRENCY_CHOICES if c[0] != ""])

    def resolve_payment_plan_status_choices(self, info, **kwargs):
        return to_choice_object(PaymentPlan.Status.choices)

    def resolve_payment_plan_background_action_status_choices(self, info, **kwargs):
        return to_choice_object(PaymentPlan.BackgroundActionStatus.choices)

    def resolve_all_cash_plans_and_payment_plans(self, info, **kwargs):
        qs = ExtendedQuerySetSequence(
            # TODO: added only for tests
            # PaymentPlan.objects.filter(status=PaymentPlan.Status.RECONCILED),
            PaymentPlan.objects.all(),
            CashPlan.objects.all(),
        )

        payment_verification_summary_qs = PaymentVerificationSummary.objects.filter(
            payment_plan_object_id=str(OuterRef("id"))
        )
        service_provider_qs = ServiceProvider.objects.filter(cash_plans=OuterRef("id")).distinct()
        # cash_plan_qs = CashPlan.objects.filter(id=OuterRef("id")).distinct()

        delivery_mechanisms_per_payment_plan_qs = DeliveryMechanismPerPaymentPlan.objects.filter(
            payment_plan=OuterRef("pk")
        )
        # fsp_ids = delivery_mechanisms_per_payment_plan_qs.values_list("financial_service_provider", flat=True)
        # fsp_qs = FinancialServiceProvider.objects.filter(id__in=fsp_ids).distinct()

        qs = qs.annotate(
            custom_order=Case(
                When(
                    Exists(payment_verification_summary_qs.filter(status=PaymentVerificationPlan.STATUS_ACTIVE)),
                    then=Value(1),
                ),
                When(
                    Exists(payment_verification_summary_qs.filter(status=PaymentVerificationPlan.STATUS_PENDING)),
                    then=Value(2),
                ),
                When(
                    Exists(payment_verification_summary_qs.filter(status=PaymentVerificationPlan.STATUS_FINISHED)),
                    then=Value(3),
                ),
                output_field=IntegerField(),
                default=Value(0),
            ),
            fsp_names=Case(
                When(
                    Exists(service_provider_qs),
                    then=Subquery(service_provider_qs.values_list("full_name", flat=True)),
                ),
                When(
                    Exists(delivery_mechanisms_per_payment_plan_qs),
                    then=Value("FSP qs"),
                    # TODO: upd query
                    # then=Subquery(fsp_qs.values_list("name", flat=True)),
                ),
                default=Value(""),
                output_field=CharField(),
            ),
            # TODO: upd 'delivery_types'
            delivery_types=Case(
                When(
                    Exists(service_provider_qs),
                    # then=F("delivery_type"),
                    then=Value("from cash_plan"),
                ),
                When(
                    Exists(delivery_mechanisms_per_payment_plan_qs),
                    then=Value("list form delivery_mechanisms_per_payment_plan")
                    # then=Subquery(delivery_mechanisms_per_payment_plan_qs.values_list("delivery_mechanism", flat=True)),
                ),
                default=Value(""),
                output_field=CharField(),
            ),
        ).order_by("-updated_at", "custom_order")

        business_area = kwargs.get("business_area")
        if business_area:
            qs = qs.filter(business_area__slug=business_area)

        order_by_value = kwargs.get("order_by")

        # ordering
        if order_by_value:
            reverse = "-" if order_by_value.startswith("-") else ""
            order_by = order_by_value[1:] if reverse else order_by_value
            # unicef_id, verification_status, start_date, program__name, updated_at
            if order_by == "verification_status":
                qs = qs.order_by(reverse + "custom_order")

            elif order_by == "unicef_id":
                qs = sorted(qs, key=lambda o: o.unicef_id, reverse=bool(reverse))
            else:
                qs = qs.order_by(reverse + order_by)

        # add qraphql pagination
        resp = connection_from_list_slice(
            qs,
            args=kwargs,
            connection_type=PaginatedCashPlanAndPaymentPlanNode,
            edge_type=CashPlanAndPaymentPlanEdges,
            pageinfo_type=PageInfoNode,
            list_length=len(qs),
        )
        resp.total_count = len(qs)

        return resp
