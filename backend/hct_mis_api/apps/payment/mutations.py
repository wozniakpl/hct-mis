import logging
import math
from base64 import b64decode
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

import graphene
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError

from hct_mis_api.apps.account.permissions import PermissionMutation, Permissions
from hct_mis_api.apps.activity_log.models import log_create
from hct_mis_api.apps.activity_log.utils import copy_model_object
from hct_mis_api.apps.core.permissions import is_authenticated
from hct_mis_api.apps.core.scalars import BigInt
from hct_mis_api.apps.core.utils import (
    check_concurrency_version_in_mutation,
    decode_id_string,
)
from hct_mis_api.apps.household.models import Individual
from hct_mis_api.apps.payment.celery_tasks import (
    create_payment_verification_plan_xlsx,
    fsp_generate_xlsx_report_task,
    import_payment_plan_payment_list_from_xlsx,
    payment_plan_apply_steficon,
)
from hct_mis_api.apps.payment.inputs import (
    ActionPaymentPlanInput,
    CreateFinancialServiceProviderInput,
    CreatePaymentPlanInput,
    CreatePaymentVerificationInput,
    EditPaymentVerificationInput,
    UpdatePaymentPlanInput,
)
from hct_mis_api.apps.payment.models import (
    CashPlan,
    DeliveryMechanismPerPaymentPlan,
    FinancialServiceProvider,
    GenericPayment,
    PaymentChannel,
    PaymentPlan,
    PaymentRecord,
    PaymentVerification,
    PaymentVerificationPlan,
)
from hct_mis_api.apps.payment.schema import (
    FinancialServiceProviderNode,
    GenericPaymentPlanNode,
    PaymentPlanNode,
    PaymentRecordNode,
    PaymentVerificationNode,
)
from hct_mis_api.apps.payment.services.fsp_service import FSPService
from hct_mis_api.apps.payment.services.mark_as_failed import mark_as_failed
from hct_mis_api.apps.payment.services.payment_plan_services import PaymentPlanService
from hct_mis_api.apps.payment.services.verification_plan_crud_services import (
    VerificationPlanCrudServices,
)
from hct_mis_api.apps.payment.services.verification_plan_status_change_services import (
    VerificationPlanStatusChangeServices,
)
from hct_mis_api.apps.payment.utils import calculate_counts, from_received_to_status
from hct_mis_api.apps.payment.xlsx.XlsxPaymentPlanImportService import (
    XlsxPaymentPlanImportService,
)
from hct_mis_api.apps.payment.xlsx.XlsxPaymentPlanPerFspImportService import (
    XlsxPaymentPlanImportPerFspService,
)
from hct_mis_api.apps.payment.xlsx.XlsxVerificationImportService import (
    XlsxVerificationImportService,
)
from hct_mis_api.apps.program.schema import CashPlanNode
from hct_mis_api.apps.steficon.models import Rule
from hct_mis_api.apps.utils.mutations import ValidationErrorMutationMixin

logger = logging.getLogger(__name__)


class CreateVerificationPlanMutation(PermissionMutation):
    payment_plan = graphene.Field(GenericPaymentPlanNode)

    class Arguments:
        input = CreatePaymentVerificationInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, input, **kwargs):
        cash_or_payment_plan_id = input.get("cash_or_payment_plan_id")
        node_name, obj_id = b64decode(cash_or_payment_plan_id).decode().split(":")

        payment_plan_object = get_object_or_404(CashPlan if node_name == "CashPlanNode" else PaymentPlan, id=obj_id)

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_CREATE, payment_plan_object.business_area)

        verification_plan = VerificationPlanCrudServices.create(payment_plan_object, input)

        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            None,
            verification_plan,
        )
        payment_plan_object.refresh_from_db()

        return cls(payment_plan=payment_plan_object)


class EditPaymentVerificationMutation(PermissionMutation):
    payment_plan = graphene.Field(GenericPaymentPlanNode)

    class Arguments:
        input = EditPaymentVerificationInput(required=True)
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, input, **kwargs):
        payment_verification_id = decode_id_string(input.get("payment_verification_plan_id"))
        payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=payment_verification_id)

        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification_plan)

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_UPDATE, payment_verification_plan.business_area)

        old_payment_verification_plan = copy_model_object(payment_verification_plan)
        payment_verification_plan.verification_channel = input.get("verification_channel")
        payment_verification_plan.payment_record_verifications.all().delete()

        payment_verification_plan = VerificationPlanCrudServices.update(payment_verification_plan, input)

        payment_verification_plan.payment_plan_obj.refresh_from_db()

        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification_plan,
            payment_verification_plan,
        )
        return cls(payment_plan=payment_verification_plan.payment_plan_obj)


class ActivatePaymentVerificationPlan(PermissionMutation, ValidationErrorMutationMixin):
    # TODO upd to GenericPaymentPlanNode
    payment_plan = graphene.Field(CashPlanNode)

    class Arguments:
        payment_verification_plan_id = graphene.ID(required=True)
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def processed_mutate(cls, root, info, payment_verification_plan_id, **kwargs):
        payment_verification_plan_id = decode_id_string(payment_verification_plan_id)
        payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=payment_verification_plan_id)

        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification_plan)

        old_payment_verification_plan = copy_model_object(payment_verification_plan)
        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_ACTIVATE, payment_verification_plan.business_area)

        payment_verification_plan = VerificationPlanStatusChangeServices(payment_verification_plan).activate()

        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification_plan,
            payment_verification_plan,
        )
        return ActivatePaymentVerificationPlan(payment_plan=payment_verification_plan.payment_plan_obj)


class FinishPaymentVerificationPlan(PermissionMutation):
    # TODO upd to GenericPaymentPlanNode
    payment_plan = graphene.Field(CashPlanNode)

    class Arguments:
        payment_verification_plan_id = graphene.ID(required=True)
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, payment_verification_plan_id, **kwargs):
        id = decode_id_string(payment_verification_plan_id)
        payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=id)
        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification_plan)
        old_payment_verification_plan = copy_model_object(payment_verification_plan)
        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_FINISH, payment_verification_plan.business_area)

        if payment_verification_plan.status != PaymentVerificationPlan.STATUS_ACTIVE:
            logger.error("You can finish only ACTIVE verification")
            raise GraphQLError("You can finish only ACTIVE verification")
        VerificationPlanStatusChangeServices(payment_verification_plan).finish()
        payment_verification_plan.refresh_from_db()
        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification_plan,
            payment_verification_plan,
        )
        return FinishPaymentVerificationPlan(payment_plan=payment_verification_plan.payment_plan_obj)


class DiscardPaymentVerificationPlan(PermissionMutation):
    # TODO upd to GenericPaymentPlanNode
    payment_plan = graphene.Field(CashPlanNode)

    class Arguments:
        payment_verification_plan_id = graphene.ID(required=True)
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, payment_verification_plan_id, **kwargs):
        payment_verification_plan_id = decode_id_string(payment_verification_plan_id)
        payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=payment_verification_plan_id)

        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification_plan)

        old_payment_verification_plan = copy_model_object(payment_verification_plan)

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_DISCARD, payment_verification_plan.business_area)

        payment_verification_plan = VerificationPlanStatusChangeServices(payment_verification_plan).discard()

        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification_plan,
            payment_verification_plan,
        )
        return cls(payment_plan=payment_verification_plan.payment_plan_obj)


class InvalidPaymentVerificationPlan(PermissionMutation):
    # TODO upd to GenericPaymentPlanNode
    payment_plan = graphene.Field(CashPlanNode)

    class Arguments:
        payment_verification_plan_id = graphene.ID(required=True)
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, payment_verification_plan_id, **kwargs):
        payment_verification_plan_id = decode_id_string(payment_verification_plan_id)
        payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=payment_verification_plan_id)

        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification_plan)

        old_payment_verification_plan = copy_model_object(payment_verification_plan)

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_INVALID, payment_verification_plan.business_area)

        payment_verification_plan = VerificationPlanStatusChangeServices(payment_verification_plan).mark_invalid()

        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification_plan,
            payment_verification_plan,
        )
        return cls(payment_plan=payment_verification_plan.payment_plan_obj)


class DeletePaymentVerificationPlan(PermissionMutation):
    # TODO upd to GenericPaymentPlanNode
    payment_plan = graphene.Field(CashPlanNode)

    class Arguments:
        payment_verification_plan_id = graphene.ID(required=True)
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, payment_verification_plan_id, **kwargs):
        payment_verification_plan_id = decode_id_string(payment_verification_plan_id)
        payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=payment_verification_plan_id)
        payment_plan = payment_verification_plan.payment_plan_obj

        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification_plan)

        old_payment_verification_plan = copy_model_object(payment_verification_plan)

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_DELETE, payment_verification_plan.business_area)

        VerificationPlanCrudServices.delete(payment_verification_plan)

        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification_plan,
            None,
        )
        return cls(payment_plan=payment_plan)


class UpdatePaymentVerificationStatusAndReceivedAmount(graphene.Mutation):
    # TODO I don't think this is being used now, add permission if in use
    payment_verification = graphene.Field(PaymentVerificationNode)

    class Arguments:
        payment_verification_id = graphene.ID(required=True)
        received_amount = graphene.Decimal(required=True)
        status = graphene.Argument(
            graphene.Enum(
                "PaymentVerificationStatusForUpdate",
                [(x[0], x[0]) for x in PaymentVerification.STATUS_CHOICES],
            )
        )
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(
        cls,
        root,
        info,
        payment_verification_id,
        received_amount,
        status,
        **kwargs,
    ):
        payment_verification = get_object_or_404(PaymentVerification, id=decode_id_string(payment_verification_id))
        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification)
        old_payment_verification = copy_model_object(payment_verification)
        if (
            payment_verification.payment_verification_plan.verification_channel
            != PaymentVerificationPlan.VERIFICATION_CHANNEL_MANUAL
        ):
            logger.error("You can only update status of payment verification for MANUAL verification method")
            raise GraphQLError("You can only update status of payment verification for MANUAL verification method")
        if payment_verification.payment_verification_plan.status != PaymentVerificationPlan.STATUS_ACTIVE:
            logger.error(
                f"You can only update status of payment verification for {PaymentVerificationPlan.STATUS_ACTIVE} cash plan verification"
            )
            raise GraphQLError(
                f"You can only update status of payment verification for {PaymentVerificationPlan.STATUS_ACTIVE} cash plan verification"
            )
        delivered_amount = payment_verification.get_payment.delivered_quantity
        if status == PaymentVerification.STATUS_PENDING and received_amount is not None:
            logger.error(
                f"Wrong status {PaymentVerification.STATUS_PENDING} when received_amount ({received_amount}) is not empty",
            )
            raise GraphQLError(
                f"Wrong status {PaymentVerification.STATUS_PENDING} when received_amount ({received_amount}) is not empty",
            )
        elif (
            status == PaymentVerification.STATUS_NOT_RECEIVED
            and received_amount is not None
            and received_amount != Decimal(0)
        ):
            logger.error(
                f"Wrong status {PaymentVerification.STATUS_NOT_RECEIVED} when received_amount ({received_amount}) is not 0 or empty",
            )
            raise GraphQLError(
                f"Wrong status {PaymentVerification.STATUS_NOT_RECEIVED} when received_amount ({received_amount}) is not 0 or empty",
            )
        elif status == PaymentVerification.STATUS_RECEIVED_WITH_ISSUES and (
            received_amount is None or received_amount == Decimal(0)
        ):
            logger.error(
                f"Wrong status {PaymentVerification.STATUS_RECEIVED_WITH_ISSUES} when received_amount ({received_amount}) is 0 or empty",
            )
            raise GraphQLError(
                f"Wrong status {PaymentVerification.STATUS_RECEIVED_WITH_ISSUES} when received_amount ({received_amount}) is 0 or empty",
            )
        elif status == PaymentVerification.STATUS_RECEIVED and received_amount != delivered_amount:
            received_amount_text = "None" if received_amount is None else received_amount
            logger.error(
                f"Wrong status {PaymentVerification.STATUS_RECEIVED} when received_amount ({received_amount_text}) ≠ delivered_amount ({delivered_amount})"
            )
            raise GraphQLError(
                f"Wrong status {PaymentVerification.STATUS_RECEIVED} when received_amount ({received_amount_text}) ≠ delivered_amount ({delivered_amount})"
            )
        payment_verification.status = status
        payment_verification.received_amount = received_amount
        payment_verification.save()
        payment_verification_plan = payment_verification.payment_verification_plan
        old_payment_verification_plan = copy_model_object(payment_verification_plan)
        calculate_counts(payment_verification_plan)
        payment_verification_plan.save()

        log_create(
            PaymentVerificationPlan.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification_plan,
            payment_verification_plan,
        )
        log_create(
            PaymentVerification.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification,
            payment_verification,
        )
        return UpdatePaymentVerificationStatusAndReceivedAmount(payment_verification)


class UpdatePaymentVerificationReceivedAndReceivedAmount(PermissionMutation):
    payment_verification = graphene.Field(PaymentVerificationNode)

    class Arguments:
        payment_verification_id = graphene.ID(required=True)
        received_amount = graphene.Decimal(required=True)
        received = graphene.Boolean(required=True)
        version = BigInt(required=False)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(
        cls,
        root,
        info,
        payment_verification_id,
        received_amount,
        received,
        **kwargs,
    ):
        if math.isnan(received_amount):
            received_amount = None
        payment_verification = get_object_or_404(PaymentVerification, id=decode_id_string(payment_verification_id))
        check_concurrency_version_in_mutation(kwargs.get("version"), payment_verification)
        old_payment_verification = copy_model_object(payment_verification)
        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_VERIFY, payment_verification.business_area)
        if (
            payment_verification.payment_verification_plan.verification_channel
            != PaymentVerificationPlan.VERIFICATION_CHANNEL_MANUAL
        ):
            logger.error("You can only update status of payment verification for MANUAL verification method")
            raise GraphQLError("You can only update status of payment verification for MANUAL verification method")
        if payment_verification.payment_verification_plan.status != PaymentVerificationPlan.STATUS_ACTIVE:
            logger.error(
                f"You can only update status of payment verification for {PaymentVerificationPlan.STATUS_ACTIVE} cash plan verification"
            )
            raise GraphQLError(
                f"You can only update status of payment verification for {PaymentVerificationPlan.STATUS_ACTIVE} cash plan verification"
            )
        if not payment_verification.is_manually_editable:
            logger.error("You can only edit payment verification in first 10 minutes")
            raise GraphQLError("You can only edit payment verification in first 10 minutes")
        delivered_amount = payment_verification.get_payment.delivered_quantity

        if received is None and received_amount is not None and received_amount == 0:
            logger.error(f"You can't set received_amount {received_amount} and not set received to NO")
            raise GraphQLError(f"You can't set received_amount {received_amount} and not set received to NO")
        if received is None and received_amount is not None:
            logger.error(f"You can't set received_amount {received_amount} and not set received to YES")
            raise GraphQLError(f"You can't set received_amount {received_amount} and not set received to YES")
        elif received_amount == 0 and received:
            logger.error(
                "If received_amount is 0, you should set received to NO",
            )
            raise GraphQLError(
                "If received_amount is 0, you should set received to NO",
            )
        elif received_amount is not None and received_amount != 0 and not received:
            logger.error(f"If received_amount({received_amount}) is not 0, you should set received to YES")
            raise GraphQLError(f"If received_amount({received_amount}) is not 0, you should set received to YES")

        payment_verification.status = from_received_to_status(received, received_amount, delivered_amount)
        payment_verification.status_date = timezone.now()
        payment_verification.received_amount = received_amount
        payment_verification.save()
        payment_verification_plan = payment_verification.payment_verification_plan
        calculate_counts(payment_verification_plan)
        payment_verification_plan.save()
        log_create(
            PaymentVerification.ACTIVITY_LOG_MAPPING,
            "business_area",
            info.context.user,
            old_payment_verification,
            payment_verification,
        )
        return UpdatePaymentVerificationStatusAndReceivedAmount(payment_verification)


class XlsxErrorNode(graphene.ObjectType):
    sheet = graphene.String()
    coordinates = graphene.String()
    message = graphene.String()

    def resolve_sheet(parent, info):
        return parent[0]

    def resolve_coordinates(parent, info):
        return parent[1]

    def resolve_message(parent, info):
        return parent[2]


class ExportXlsxPaymentVerificationPlanFile(PermissionMutation):
    # TODO upd to GenericPaymentPlanNode
    payment_plan = graphene.Field(CashPlanNode)

    class Arguments:
        payment_verification_plan_id = graphene.ID(required=True)

    @classmethod
    @is_authenticated
    def mutate(cls, root, info, payment_verification_plan_id):
        pk = decode_id_string(payment_verification_plan_id)
        payment_verification_plan = get_object_or_404(PaymentVerificationPlan, id=pk)

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_EXPORT, payment_verification_plan.business_area)

        if payment_verification_plan.status != PaymentVerificationPlan.STATUS_ACTIVE:
            logger.error("You can only export verification for active CashPlan verification")
            raise GraphQLError("You can export verification for active CashPlan verification")
        if payment_verification_plan.verification_channel != PaymentVerificationPlan.VERIFICATION_CHANNEL_XLSX:
            logger.error("You can only export verification when XLSX channel is selected")
            raise GraphQLError("You can export verification when XLSX channel is selected")
        if payment_verification_plan.xlsx_file_exporting:
            logger.error("Exporting xlsx file is already started. Please wait")
            raise GraphQLError("Exporting xlsx file is already started. Please wait")
        if payment_verification_plan.has_xlsx_payment_verification_plan_file:
            logger.error("Xlsx file is already created")
            raise GraphQLError("Xlsx file is already created")

        payment_verification_plan.xlsx_file_exporting = True
        payment_verification_plan.save()
        create_payment_verification_plan_xlsx.delay(pk, info.context.user.pk)
        return cls(payment_plan=payment_verification_plan.payment_plan_obj)


class ImportXlsxPaymentVerificationPlanFile(PermissionMutation):
    # TODO upd to GenericPaymentPlanNode
    payment_plan = graphene.Field(CashPlanNode)
    errors = graphene.List(XlsxErrorNode)

    class Arguments:
        file = Upload(required=True)
        payment_verification_plan_id = graphene.ID(required=True)

    @classmethod
    @is_authenticated
    def mutate(cls, root, info, file, payment_verification_plan_id):
        id = decode_id_string(payment_verification_plan_id)
        cashplan_payment_verification = get_object_or_404(PaymentVerificationPlan, id=id)

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_IMPORT, cashplan_payment_verification.business_area)

        if cashplan_payment_verification.status != PaymentVerificationPlan.STATUS_ACTIVE:
            logger.error("You can only import verification for active CashPlan verification")
            raise GraphQLError("You can only import verification for active CashPlan verification")
        if cashplan_payment_verification.verification_channel != PaymentVerificationPlan.VERIFICATION_CHANNEL_XLSX:
            logger.error("You can only import verification when XLSX channel is selected")
            raise GraphQLError("You can only import verification when XLSX channel is selected")
        import_service = XlsxVerificationImportService(cashplan_payment_verification, file)
        import_service.open_workbook()
        import_service.validate()
        if len(import_service.errors):
            return ImportXlsxPaymentVerificationPlanFile(None, import_service.errors)
        import_service.import_verifications()
        calculate_counts(cashplan_payment_verification)
        cashplan_payment_verification.xlsx_file_imported = True
        cashplan_payment_verification.save()
        return ImportXlsxPaymentVerificationPlanFile(cashplan_payment_verification.payment_plan, import_service.errors)


class MarkPaymentRecordAsFailedMutation(PermissionMutation):
    payment_record = graphene.Field(PaymentRecordNode)

    class Arguments:
        payment_record_id = graphene.ID(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(
        cls,
        root,
        info,
        payment_record_id,
        **kwargs,
    ):
        payment_record = get_object_or_404(PaymentRecord, id=decode_id_string(payment_record_id))

        cls.has_permission(info, Permissions.PAYMENT_VERIFICATION_MARK_AS_FAILED, payment_record.business_area)

        try:
            mark_as_failed(payment_record)
        except ValidationError as e:
            logger.error(e.message)
            raise GraphQLError(e.message) from e

        return MarkPaymentRecordAsFailedMutation(payment_record)


class CreateFinancialServiceProviderMutation(PermissionMutation):
    financial_service_provider = graphene.Field(FinancialServiceProviderNode)

    class Arguments:
        business_area_slug = graphene.String(required=True)
        inputs = CreateFinancialServiceProviderInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, business_area_slug, inputs):
        cls.has_permission(info, Permissions.FINANCIAL_SERVICE_PROVIDER_CREATE, business_area_slug)

        fsp = FSPService.create(inputs, info.context.user)
        # Schedule task to generate downloadable report
        fsp_generate_xlsx_report_task.delay(fsp.id)

        return cls(financial_service_provider=fsp)


class EditFinancialServiceProviderMutation(PermissionMutation):
    financial_service_provider = graphene.Field(FinancialServiceProviderNode)

    class Arguments:
        business_area_slug = graphene.String(required=True)
        financial_service_provider_id = graphene.ID(required=True)
        inputs = CreateFinancialServiceProviderInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, business_area_slug, financial_service_provider_id, inputs):
        cls.has_permission(info, Permissions.FINANCIAL_SERVICE_PROVIDER_UPDATE, business_area_slug)

        fsp_id = decode_id_string(financial_service_provider_id)
        fsp = FSPService.update(fsp_id, inputs)
        fsp_generate_xlsx_report_task.delay(fsp_id)

        return cls(financial_service_provider=fsp)


class ActionPaymentPlanMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Arguments:
        input = ActionPaymentPlanInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, input, **kwargs):
        payment_plan_id = decode_id_string(input.get("payment_plan_id"))
        payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
        old_payment_plan = copy_model_object(payment_plan)

        # TODO: maybe will update perms here?
        cls.has_permission(info, Permissions.PAYMENT_MODULE_VIEW_DETAILS, payment_plan.business_area)

        payment_plan = PaymentPlanService(payment_plan).execute_update_status_action(
            input_data=input, user=info.context.user
        )

        log_create(
            mapping=PaymentPlan.ACTIVITY_LOG_MAPPING,
            business_area_field="business_area",
            user=info.context.user,
            old_object=old_payment_plan,
            new_object=payment_plan,
        )
        return cls(payment_plan=payment_plan)


class CreatePaymentPlanMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Arguments:
        input = CreatePaymentPlanInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, input, **kwargs):
        cls.has_permission(info, Permissions.PAYMENT_MODULE_CREATE, input.get("business_area_slug"))

        payment_plan = PaymentPlanService().create(input_data=input, user=info.context.user)

        log_create(
            mapping=PaymentPlan.ACTIVITY_LOG_MAPPING,
            business_area_field="business_area",
            user=info.context.user,
            new_object=payment_plan,
        )
        return cls(payment_plan=payment_plan)


class UpdatePaymentPlanMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Arguments:
        input = UpdatePaymentPlanInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, input, **kwargs):
        payment_plan_id = decode_id_string(input.get("payment_plan_id"))
        payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
        old_payment_plan = copy_model_object(payment_plan)

        cls.has_permission(info, Permissions.PAYMENT_MODULE_CREATE, payment_plan.business_area)

        payment_plan = PaymentPlanService(payment_plan=payment_plan).update(input_data=input)

        log_create(
            mapping=PaymentPlan.ACTIVITY_LOG_MAPPING,
            business_area_field="business_area",
            user=info.context.user,
            old_object=old_payment_plan,
            new_object=payment_plan,
        )

        return cls(payment_plan=payment_plan)


class DeletePaymentPlanMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Arguments:
        payment_plan_id = graphene.ID(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, payment_plan_id, **kwargs):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(payment_plan_id))

        old_payment_plan = copy_model_object(payment_plan)

        cls.has_permission(info, Permissions.PAYMENT_MODULE_CREATE, payment_plan.business_area)

        payment_plan = PaymentPlanService(payment_plan=payment_plan).delete()

        log_create(
            mapping=PaymentPlan.ACTIVITY_LOG_MAPPING,
            business_area_field="business_area",
            user=info.context.user,
            old_object=old_payment_plan,
            new_object=payment_plan,
        )

        return cls(payment_plan=payment_plan)


class ChooseDeliveryMechanismsForPaymentPlanInput(graphene.InputObjectType):
    payment_plan_id = graphene.ID(required=True)
    delivery_mechanisms = graphene.List(graphene.String, required=True)


class ExportXLSXPaymentPlanPaymentListMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Arguments:
        payment_plan_id = graphene.ID(required=True)

    @classmethod
    def export_action(cls, payment_plan: PaymentPlan, user) -> PaymentPlan:
        if payment_plan.status not in [PaymentPlan.Status.LOCKED]:
            msg = "You can only export Payment List for LOCKED Payment Plan"
            logger.error(msg)
            raise GraphQLError(msg)

        return PaymentPlanService(payment_plan=payment_plan).export_xlsx(user=user)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, payment_plan_id, **kwargs):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(payment_plan_id))
        cls.has_permission(info, Permissions.PAYMENT_MODULE_VIEW_LIST, payment_plan.business_area)

        old_payment_plan = copy_model_object(payment_plan)

        payment_plan = cls.export_action(payment_plan=payment_plan, user=info.context.user)

        log_create(
            mapping=PaymentPlan.ACTIVITY_LOG_MAPPING,
            business_area_field="business_area",
            user=info.context.user,
            old_object=old_payment_plan,
            new_object=payment_plan,
        )

        return cls(payment_plan=payment_plan)


class ExportXLSXPaymentPlanPaymentListPerFSPMutation(ExportXLSXPaymentPlanPaymentListMutation):
    @classmethod
    def export_action(cls, payment_plan: PaymentPlan, user) -> PaymentPlan:
        if payment_plan.status != PaymentPlan.Status.ACCEPTED:
            msg = "You can only export Payment List Per FSP for ACCEPTED Payment Plan"
            logger.error(msg)
            raise GraphQLError(msg)

        if not payment_plan.not_excluded_payments:
            msg = "Export is not impossible because Payment list is empty"
            logger.error(msg)
            raise GraphQLError(msg)

        return PaymentPlanService(payment_plan=payment_plan).export_xlsx_per_fsp(user=user)


def create_insufficient_delivery_mechanisms_message(collectors_that_cant_be_paid, delivery_mechanisms_in_order):
    needed_delivery_mechanisms = list(
        PaymentChannel.objects.filter(
            individual__in=collectors_that_cant_be_paid,
        )
        .exclude(delivery_mechanism__in=delivery_mechanisms_in_order)
        .values_list("delivery_mechanism", flat=True)
        .distinct()
    )
    if (
        GenericPayment.DELIVERY_TYPE_CASH not in delivery_mechanisms_in_order
        and collectors_that_cant_be_paid.filter(payment_channels__isnull=True).exists()
    ):
        needed_delivery_mechanisms.append(GenericPayment.DELIVERY_TYPE_CASH)
    return f"Delivery mechanisms that may be needed: {', '.join(needed_delivery_mechanisms)}."


class ChooseDeliveryMechanismsForPaymentPlanMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Arguments:
        input = ChooseDeliveryMechanismsForPaymentPlanInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, input, **kwargs):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(input.get("payment_plan_id")))
        cls.has_permission(info, Permissions.PAYMENT_MODULE_CREATE, payment_plan.business_area)
        if payment_plan.status != PaymentPlan.Status.LOCKED:
            raise GraphQLError("Payment plan must be locked to choose delivery mechanisms")
        delivery_mechanisms_in_order = input.get("delivery_mechanisms")
        for delivery_mechanism in delivery_mechanisms_in_order:
            if delivery_mechanism == "":
                raise GraphQLError("Delivery mechanism cannot be empty.")
            if delivery_mechanism not in [choice[0] for choice in GenericPayment.DELIVERY_TYPE_CHOICE]:
                raise GraphQLError(f"Delivery mechanism '{delivery_mechanism}' is not valid.")
        collectors_in_target_population = Individual.objects.filter(
            id__in=payment_plan.not_excluded_payments.values_list("collector", flat=True)
        )

        query = Q(payment_channels__delivery_mechanism__in=delivery_mechanisms_in_order)
        if GenericPayment.DELIVERY_TYPE_CASH in delivery_mechanisms_in_order:
            query |= Q(payment_channels__isnull=True)

        collectors_that_can_be_paid = collectors_in_target_population.filter(query).distinct()
        collectors_that_cant_be_paid = collectors_in_target_population.exclude(id__in=collectors_that_can_be_paid)

        if collectors_that_cant_be_paid.exists():
            raise GraphQLError(
                "Selected delivery mechanisms are not sufficient to serve all beneficiaries. "
                f"{create_insufficient_delivery_mechanisms_message(collectors_that_cant_be_paid, delivery_mechanisms_in_order)}"
            )

        DeliveryMechanismPerPaymentPlan.objects.filter(payment_plan=payment_plan).delete()
        current_time = timezone.now()
        for index, delivery_mechanism in enumerate(delivery_mechanisms_in_order):
            DeliveryMechanismPerPaymentPlan.objects.update_or_create(
                payment_plan=payment_plan,
                delivery_mechanism=delivery_mechanism,
                sent_date=current_time,
                delivery_mechanism_order=index + 1,
                created_by=info.context.user,
            )

        cash_fallback_payment_collectors = collectors_that_can_be_paid.filter(payment_channels__isnull=True)
        payment_channels_to_create = []
        for collector in cash_fallback_payment_collectors:
            # TODO handle delivery data
            payment_channels_to_create.append(
                PaymentChannel(
                    individual=collector, delivery_mechanism=GenericPayment.DELIVERY_TYPE_CASH, is_fallback=True
                )
            )
        PaymentChannel.objects.bulk_create(payment_channels_to_create)

        return cls(payment_plan=payment_plan)


class FSPToDeliveryMechanismMappingInput(graphene.InputObjectType):
    fsp_id = graphene.ID(required=True)
    delivery_mechanism = graphene.String(required=True)
    order = graphene.Int(required=True)


class AssignFspToDeliveryMechanismInput(graphene.InputObjectType):
    payment_plan_id = graphene.ID(required=True)
    mappings = graphene.List(FSPToDeliveryMechanismMappingInput, required=True)


class AssignFspToDeliveryMechanismMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Arguments:
        input = AssignFspToDeliveryMechanismInput(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, input, **kwargs):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(input.get("payment_plan_id")))
        cls.has_permission(info, Permissions.PAYMENT_MODULE_CREATE, payment_plan.business_area)
        if payment_plan.status != PaymentPlan.Status.LOCKED:
            raise GraphQLError("Payment plan must be locked to assign FSP to delivery mechanism")

        mappings = input.get("mappings", [])

        if len(mappings) != payment_plan.delivery_mechanisms.count():
            raise GraphQLError("Please assign FSP to all delivery mechanisms before moving to next step")

        existing_pairs = set()
        for mapping in mappings:
            key = (mapping["fsp_id"], mapping["delivery_mechanism"])
            if key in existing_pairs:
                raise GraphQLError("You can't assign the same FSP to the same delivery mechanism more than once")
            existing_pairs.add(key)

        dm_to_fsp_mapping = [
            {
                "fsp": get_object_or_404(FinancialServiceProvider, id=decode_id_string(mapping["fsp_id"])),
                "delivery_mechanism_per_payment_plan": get_object_or_404(
                    DeliveryMechanismPerPaymentPlan,
                    payment_plan=payment_plan,
                    delivery_mechanism=mapping["delivery_mechanism"],
                    delivery_mechanism_order=mapping["order"],
                ),
            }
            for mapping in mappings
        ]

        with transaction.atomic():
            payment_plan.delivery_mechanisms.all().update(financial_service_provider=None)

            payment_plan_service = PaymentPlanService(payment_plan=payment_plan)
            payment_plan_service.validate_fsps_per_delivery_mechanisms(
                dm_to_fsp_mapping, update_dms=True, update_payments=False
            )

        return cls(payment_plan=payment_plan)


class ImportXLSXPaymentPlanPaymentListMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)
    errors = graphene.List(XlsxErrorNode)

    class Arguments:
        file = Upload(required=True)
        payment_plan_id = graphene.ID(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, file, payment_plan_id):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(payment_plan_id))

        cls.has_permission(info, Permissions.PAYMENT_MODULE_VIEW_LIST, payment_plan.business_area)

        if payment_plan.status != PaymentPlan.Status.LOCKED:
            msg = "You can only import for LOCKED Payment Plan"
            logger.error(msg)
            raise GraphQLError(msg)

        if payment_plan.background_action_status == PaymentPlan.BackgroundActionStatus.XLSX_IMPORTING_ENTITLEMENTS:
            msg = "Import in progress"
            logger.error(msg)
            raise GraphQLError(msg)

        with transaction.atomic():
            import_service = XlsxPaymentPlanImportService(payment_plan, file)
            import_service.open_workbook()
            import_service.validate()
            if import_service.errors:
                return cls(None, import_service.errors)

            payment_plan.background_action_status_xlsx_importing_entitlements()
            payment_plan.save()

            import_service.create_import_xlsx_file(info.context.user)

            transaction.on_commit(lambda: import_payment_plan_payment_list_from_xlsx.delay(payment_plan.id))

        return cls(payment_plan, None)


class ImportXLSXPaymentPlanPaymentListPerFSPMutation(PermissionMutation):
    # PaymentPlan Reconciliation
    payment_plan = graphene.Field(PaymentPlanNode)
    errors = graphene.List(XlsxErrorNode)

    class Arguments:
        file = Upload(required=True)
        payment_plan_id = graphene.ID(required=True)

    @classmethod
    @is_authenticated
    @transaction.atomic
    def mutate(cls, root, info, file, payment_plan_id):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(payment_plan_id))

        cls.has_permission(info, Permissions.PAYMENT_MODULE_VIEW_LIST, payment_plan.business_area)

        if payment_plan.status != PaymentPlan.Status.ACCEPTED:
            msg = "You can only import for ACCEPTED Payment Plan"
            logger.error(msg)
            raise GraphQLError(msg)

        import_service = XlsxPaymentPlanImportPerFspService(payment_plan, file)
        import_service.open_workbook()
        import_service.validate()
        if import_service.errors:
            return cls(payment_plan=None, errors=import_service.errors)

        payment_plan = PaymentPlanService(payment_plan=payment_plan).import_xlsx_per_fsp(
            user=info.context.user, file=file
        )

        return cls(payment_plan=payment_plan, errors=None)


class SetSteficonRuleOnPaymentPlanPaymentListMutation(PermissionMutation):
    payment_plan = graphene.Field(PaymentPlanNode)

    class Input:
        payment_plan_id = graphene.ID(required=True)
        steficon_rule_id = graphene.ID(required=True)

    @classmethod
    @is_authenticated
    def mutate(cls, root, info, payment_plan_id, steficon_rule_id):
        payment_plan = get_object_or_404(PaymentPlan, id=decode_id_string(payment_plan_id))

        cls.has_permission(info, Permissions.PAYMENT_MODULE_VIEW_LIST, payment_plan.business_area)

        if payment_plan.status != PaymentPlan.Status.LOCKED:
            msg = "You can run formula only for 'Locked' status of Payment Plan"
            logger.error(msg)
            raise GraphQLError(msg)

        if payment_plan.background_action_status == PaymentPlan.BackgroundActionStatus.STEFICON_RUN:
            msg = "Steficon run in progress"
            logger.error(msg)
            raise GraphQLError(msg)

        old_payment_plan = copy_model_object(payment_plan)

        steficon_rule = get_object_or_404(Rule, id=decode_id_string(steficon_rule_id))
        if not steficon_rule.enabled or steficon_rule.deprecated:
            msg = "This steficon rule is not enabled or is deprecated."
            logger.error(msg)
            raise GraphQLError(msg)

        payment_plan_apply_steficon.delay(payment_plan.pk, steficon_rule_id)

        log_create(
            mapping=PaymentPlan.ACTIVITY_LOG_MAPPING,
            business_area_field="business_area",
            user=info.context.user,
            old_object=old_payment_plan,
            new_object=payment_plan,
        )
        return cls(payment_plan=payment_plan)


class Mutations(graphene.ObjectType):
    create_payment_verification_plan = CreateVerificationPlanMutation.Field()
    edit_payment_verification_plan = EditPaymentVerificationMutation.Field()

    create_financial_service_provider = CreateFinancialServiceProviderMutation.Field()
    edit_financial_service_provider = EditFinancialServiceProviderMutation.Field()
    export_xlsx_payment_verification_plan_file = ExportXlsxPaymentVerificationPlanFile.Field()
    import_xlsx_payment_verification_plan_file = ImportXlsxPaymentVerificationPlanFile.Field()
    activate_payment_verification_plan = ActivatePaymentVerificationPlan.Field()
    finish_payment_verification_plan = FinishPaymentVerificationPlan.Field()
    discard_payment_verification_plan = DiscardPaymentVerificationPlan.Field()
    invalid_payment_verification_plan = InvalidPaymentVerificationPlan.Field()
    delete_payment_verification_plan = DeletePaymentVerificationPlan.Field()
    choose_delivery_mechanisms_for_payment_plan = ChooseDeliveryMechanismsForPaymentPlanMutation.Field()
    assign_fsp_to_delivery_mechanism = AssignFspToDeliveryMechanismMutation.Field()
    update_payment_verification_status_and_received_amount = UpdatePaymentVerificationStatusAndReceivedAmount.Field()
    mark_payment_record_as_failed = MarkPaymentRecordAsFailedMutation.Field()
    update_payment_verification_received_and_received_amount = (
        UpdatePaymentVerificationReceivedAndReceivedAmount.Field()
    )
    action_payment_plan_mutation = ActionPaymentPlanMutation.Field()
    create_payment_plan = CreatePaymentPlanMutation.Field()
    update_payment_plan = UpdatePaymentPlanMutation.Field()
    delete_payment_plan = DeletePaymentPlanMutation.Field()

    export_xlsx_payment_plan_payment_list = ExportXLSXPaymentPlanPaymentListMutation.Field()
    export_xlsx_payment_plan_payment_list_per_fsp = ExportXLSXPaymentPlanPaymentListPerFSPMutation.Field()
    import_xlsx_payment_plan_payment_list = ImportXLSXPaymentPlanPaymentListMutation.Field()
    import_xlsx_payment_plan_payment_list_per_fsp = ImportXLSXPaymentPlanPaymentListPerFSPMutation.Field()
    set_steficon_rule_on_payment_plan_payment_list = SetSteficonRuleOnPaymentPlanPaymentListMutation.Field()
