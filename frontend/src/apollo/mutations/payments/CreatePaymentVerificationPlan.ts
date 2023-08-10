import { gql } from 'apollo-boost';

export const CREATE_PAYMENT_VERIFICATION_MUTATION = gql`
  mutation CreatePaymentVerificationPlan(
    $input: CreatePaymentVerificationInput!
    $version: BigInt
  ) {
    createPaymentVerificationPlan(input: $input, version: $version) {
      paymentPlan {
        id
      }
    }
  }
`;
