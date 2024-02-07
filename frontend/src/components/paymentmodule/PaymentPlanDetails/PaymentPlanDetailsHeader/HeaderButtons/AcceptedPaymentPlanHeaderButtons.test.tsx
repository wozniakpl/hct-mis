import { MockedProvider } from '@apollo/react-testing';
import { act } from 'react-dom/test-utils';
import wait from 'waait';
import * as React from 'react';
import { fakeApolloPaymentPlan } from '../../../../../../fixtures/paymentmodule/fakeApolloPaymentPlan';
import { fakeExportXlsxPpListPerFspMutation } from '../../../../../../fixtures/paymentmodule/fakeExportXlsxPpListPerFspMutation';
import { render } from '../../../../../testUtils/testUtils';
import { AcceptedPaymentPlanHeaderButtons } from './AcceptedPaymentPlanHeaderButtons';

describe('components/paymentmodule/PaymentPlanDetails/PaymentPlanDetailsHeader/HeaderButtons/AcceptedPaymentPlanHeaderButtons', () => {
  it('should render disabled buttons', async () => {
    const { container } = render(
      <MockedProvider
        addTypename={false}
        mocks={fakeExportXlsxPpListPerFspMutation}
      >
        <AcceptedPaymentPlanHeaderButtons
          canDownloadXlsx={false}
          canExportXlsx={false}
          canSendToFsp={false}
          paymentPlan={fakeApolloPaymentPlan}
        />
      </MockedProvider>,
    );
    await act(() => wait(0)); // wait for response

    expect(container).toMatchSnapshot();
  });

  it('should render not disabled buttons', async () => {
    const { container } = render(
      <MockedProvider
        addTypename={false}
        mocks={fakeExportXlsxPpListPerFspMutation}
      >
        <AcceptedPaymentPlanHeaderButtons
          canDownloadXlsx
          canExportXlsx
          canSendToFsp
          paymentPlan={fakeApolloPaymentPlan}
        />
      </MockedProvider>,
    );
    await act(() => wait(0)); // wait for response

    expect(container).toMatchSnapshot();
  });
});
