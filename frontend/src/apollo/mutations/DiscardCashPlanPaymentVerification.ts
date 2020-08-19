import { gql } from 'apollo-boost';

export const DISCARD_CASH_PLAN_PAYMENT_VERIFICATION = gql`
  mutation DiscardCashPlanPaymentVerification($cashPlanVerificationId: ID!) {
    discardCashPlanPaymentVerification(
      cashPlanVerificationId: $cashPlanVerificationId
    ) {
      cashPlan {
        id
        status
        statusDate
      }
    }
  }
`;
