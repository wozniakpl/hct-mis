import { act } from '@testing-library/react';
import React from 'react';
import wait from 'waait';
import { MockedProvider } from '@apollo/react-testing';
import { render } from '../../../../testUtils/testUtils';
import { fakeDeliveryMechanisms } from '../../../../../fixtures/payments/fakeDeliveryMechanisms';
import { fakeChooseDeliveryMechForPaymentPlanMutation } from '../../../../../fixtures/payments/fakeChooseDeliveryMechForPaymentPlanMutation';
import { PERMISSIONS } from '../../../../config/permissions';
import { SetUpFspCore } from './SetUpFspCore';

describe('components/paymentmodule/CreateSetUpFsp/SetUpFspCore', () => {
  it('should render', async () => {
    
    const { container } = render(
      <MockedProvider
        addTypename={false}
        mocks={fakeChooseDeliveryMechForPaymentPlanMutation}
      >
      <SetUpFspCore
        businessArea='afghanistan'
        permissions={[PERMISSIONS.FINANCIAL_SERVICE_PROVIDER_REMOVE]}
        initialValues={{
          deliveryMechanisms: [
            {
              deliveryMechanism: '',
              fsp: '',
            },
          ],
        }}
        setDeliveryMechanismsForQuery={(deliveryMechanisms) => {
          console.log(deliveryMechanisms);
        }}
        deliveryMechanismsForQuery={fakeDeliveryMechanisms.allDeliveryMechanisms.map((dm) => {
          return dm.name;
        })} />
        </MockedProvider>,
    );
    await act(() => wait(0)); // wait for response
    expect(container).toMatchSnapshot();
  });
});
