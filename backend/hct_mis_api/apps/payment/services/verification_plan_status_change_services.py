from graphql import GraphQLError

from hct_mis_api.apps.household.models import Individual
from hct_mis_api.apps.payment.models import (
    CashPlanPaymentVerification,
    PaymentVerification,
)
from hct_mis_api.apps.payment.services.rapid_pro.api import RapidProAPI


class VerificationPlanStatusChangeServices:
    def __init__(self, cash_plan_verification: CashPlanPaymentVerification):
        self.cash_plan_verification = cash_plan_verification

    def discard(self) -> CashPlanPaymentVerification:
        if self.cash_plan_verification.status != CashPlanPaymentVerification.STATUS_ACTIVE:
            raise GraphQLError("You can discard only ACTIVE verification")

        self.cash_plan_verification.set_pending()
        self.cash_plan_verification.save()

        # payment verifications to reset
        payment_record_verifications = self.cash_plan_verification.payment_record_verifications.all()
        for payment_record_verification in payment_record_verifications:
            payment_record_verification.set_pending()

        PaymentVerification.objects.bulk_update(
            payment_record_verifications, ["status_date", "status", "received_amount"]
        )

        return self.cash_plan_verification

    def activate(self) -> CashPlanPaymentVerification:
        if self.cash_plan_verification.status != CashPlanPaymentVerification.STATUS_PENDING:
            raise GraphQLError("You can activate only PENDING verification")

        if self._can_activate_via_rapidpro():
            self._activate_rapidpro()

        self.cash_plan_verification.set_active()
        self.cash_plan_verification.save()

        return self.cash_plan_verification

    def _can_activate_via_rapidpro(self):
        return self.cash_plan_verification.verification_method == CashPlanPaymentVerification.VERIFICATION_METHOD_RAPIDPRO

    def _activate_rapidpro(self):
        business_area_slug = self.cash_plan_verification.business_area.slug
        api = RapidProAPI(business_area_slug)
        pv_id = self.cash_plan_verification.id
        phone_numbers = list(
            Individual.objects.filter(
                heading_household__payment_records__verifications__cash_plan_payment_verification=pv_id
            ).values_list("phone_no", flat=True)
        )
        flow_start_info = api.start_flow(self.cash_plan_verification.rapid_pro_flow_id, phone_numbers)
        self.cash_plan_verification.rapid_pro_flow_start_uuid = flow_start_info.get("uuid")