import React, { ReactElement } from 'react';
import { TableWrapper } from '../../../components/core/TableWrapper';
import {
  AllFeedbacksQueryVariables,
  FeedbackNode,
  useAllFeedbacksQuery,
} from '../../../__generated__/graphql';
import { UniversalTable } from '../UniversalTable';
import { headCells } from './FeedbackTableHeadCells';
import { FeedbackTableRow } from './FeedbackTableRow';

interface FeedbackTableProps {
  filter;
  businessArea: string;
  canViewDetails: boolean;
}

export const FeedbackTable = ({
  filter,
  businessArea,
  canViewDetails,
}: FeedbackTableProps): ReactElement => {
  const initialVariables: AllFeedbacksQueryVariables = {
    feedbackId: filter.feedbackId,
    createdBy: filter.createdBy || '',
    createdAtRange: filter.createdAtRange
      ? JSON.stringify(filter.createdAtRange)
      : '',
    businessAreaSlug: businessArea,
  };
  return (
    <TableWrapper>
      <UniversalTable<FeedbackNode, AllFeedbacksQueryVariables>
        headCells={headCells}
        rowsPerPageOptions={[10, 15, 20]}
        query={useAllFeedbacksQuery}
        queriedObjectName='allFeedbacks'
        defaultOrderBy='createdAt'
        defaultOrderDirection='desc'
        initialVariables={initialVariables}
        renderRow={(row) => (
          <FeedbackTableRow
            key={row.id}
            feedback={row}
            canViewDetails={canViewDetails}
          />
        )}
      />
    </TableWrapper>
  );
};
