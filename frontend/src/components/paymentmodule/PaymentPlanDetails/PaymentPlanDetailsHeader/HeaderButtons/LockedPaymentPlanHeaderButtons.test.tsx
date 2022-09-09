import { MockedProvider } from '@apollo/react-testing';
import React from 'react';
import { act } from 'react-dom/test-utils';
import wait from 'waait';
import { fakeApolloPaymentPlan } from '../../../../../../fixtures/paymentmodule/fakeApolloPaymentPlan';
import { fakeActionPpMutation } from '../../../../../../fixtures/paymentmodule/fakeApolloActionPaymentPlanMutation';
import { render } from '../../../../../testUtils/testUtils';
import { LockedPaymentPlanHeaderButtons } from './LockedPaymentPlanHeaderButtons';

describe('components/paymentmodule/PaymentPlanDetails/PaymentPlanDetailsHeader/HeaderButtons/LockedPaymentPlanHeaderButtons', () => {
  it('should render with buttons', async () => {
    const { container } = render(
      <MockedProvider addTypename={false} mocks={fakeActionPpMutation}>
        <LockedPaymentPlanHeaderButtons
          paymentPlan={fakeApolloPaymentPlan}
          canLock
          canSendForApproval
        />
      </MockedProvider>,
    );

    await act(() => wait(0)); // wait for the mutation to complete

    expect(container).toMatchSnapshot();
  });
});
