import React, { ReactElement } from 'react';
import {
  AllCashPlansQuery,
  AllCashPlansQueryVariables,
  CashPlanNode,
  useAllCashPlansQuery,
} from '../../../__generated__/graphql';
import { UniversalTable } from '../UniversalTable';
import { headCells } from './PaymentVerificationHeadCells';
import { PaymentVerificationTableRow } from './PaymentVerificationTableRow';

interface PaymentVerificationTableProps {
  filter;
  businessArea: string;
  canViewDetails: boolean;
}
export function PaymentVerificationTable({
  filter,
  canViewDetails,
  businessArea,
}: PaymentVerificationTableProps): ReactElement {
  const initialVariables: AllCashPlansQueryVariables = {
    businessArea,
    program: filter.program,
    search: filter.search,
    serviceProvider: filter.serviceProvider,
    deliveryType: filter.deliveryType,
    verificationStatus: filter.verificationStatus,
    startDateGte: filter.startDate,
    endDateLte: filter.endDate,
  };
  return (
    <UniversalTable<AllCashPlansQuery['allCashPlans']['edges'][number]['node'], AllCashPlansQueryVariables>
      title='List of Cash Plans'
      headCells={headCells}
      query={useAllCashPlansQuery}
      queriedObjectName='allCashPlans'
      initialVariables={initialVariables}
      renderRow={(row) => (
        <PaymentVerificationTableRow
          key={row.id}
          plan={row}
          canViewDetails={canViewDetails}
        />
      )}
    />
  );
}
