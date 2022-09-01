import { MockedProvider } from '@apollo/react-testing';
import React from 'react';
import { act } from 'react-dom/test-utils';
import wait from 'waait';
import { fakeApolloPaymentPlan } from '../../../../../fixtures/payments/fakeApolloPaymentPlan';
import { fakeActionPpMutation } from '../../../../../fixtures/payments/fakeApolloActionPaymentPlanMutation';
import { render } from '../../../../testUtils/testUtils';
import { LockPaymentPlan } from './LockPaymentPlan';

describe(
  'components/paymentmodule/PaymentPlanDetails/PaymentPlanDetailsHeader/LockPaymentPlan',
  () => {
    it('should render', async () => {
      const { container } = render(
        <MockedProvider
          addTypename={false}
          mocks={fakeActionPpMutation}
        >
          <LockPaymentPlan paymentPlan={fakeApolloPaymentPlan} />
        </MockedProvider>
        ,
      );

      await act(() => wait(0)); // wait for the mutation to complete

      expect(container).toMatchSnapshot();
    });
  });
