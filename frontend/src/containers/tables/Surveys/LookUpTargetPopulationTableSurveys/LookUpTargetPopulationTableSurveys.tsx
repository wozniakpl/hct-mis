import React, { ReactElement } from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import {
  AllActiveTargetPopulationsQueryVariables,
  TargetPopulationNode,
  TargetPopulationStatus,
  useAllActiveTargetPopulationsQuery,
} from '../../../../__generated__/graphql';
import { TableWrapper } from '../../../../components/core/TableWrapper';
import { useBaseUrl } from '../../../../hooks/useBaseUrl';
import { UniversalTable } from '../../UniversalTable';
import { headCells } from './LookUpTargetPopulationTableHeadCellsSurveys';
import { LookUpTargetPopulationTableRowSurveys } from './LookUpTargetPopulationTableRowSurveys';

interface LookUpTargetPopulationTableSurveysProps {
  filter;
  canViewDetails: boolean;
  enableRadioButton?: boolean;
  selectedTargetPopulation?;
  handleChange?;
  noTableStyling?;
  noTitle?;
}

const NoTableStyling = styled.div`
  .MuiPaper-elevation1 {
    box-shadow: none;
    padding: 0 !important;
  }
`;

export const LookUpTargetPopulationTableSurveys = ({
  filter,
  canViewDetails,
  enableRadioButton,
  selectedTargetPopulation,
  handleChange,
  noTableStyling,
  noTitle,
}: LookUpTargetPopulationTableSurveysProps): ReactElement => {
  const { t } = useTranslation();
  const { businessArea, programId } = useBaseUrl();
  const initialVariables: AllActiveTargetPopulationsQueryVariables = {
    name: filter.name,
    totalHouseholdsCountMin: filter.totalHouseholdsCountMin,
    totalHouseholdsCountMax: filter.totalHouseholdsCountMax,
    status: filter.status,
    businessArea,
    program: [programId],
    createdAtRange: JSON.stringify({
      min: filter.createdAtRangeMin,
      max: filter.createdAtRangeMax,
    }),
    statusNot: TargetPopulationStatus.Open,
  };

  const handleRadioChange = (id: string): void => {
    handleChange(id);
  };

  const renderTable = (): React.ReactElement => {
    return (
      <TableWrapper>
        <UniversalTable<
          TargetPopulationNode,
          AllActiveTargetPopulationsQueryVariables
        >
          title={noTitle ? null : t('Target Populations')}
          headCells={enableRadioButton ? headCells : headCells.slice(1)}
          rowsPerPageOptions={[10, 15, 20]}
          query={useAllActiveTargetPopulationsQuery}
          queriedObjectName='allActiveTargetPopulations'
          defaultOrderBy='createdAt'
          defaultOrderDirection='desc'
          initialVariables={initialVariables}
          renderRow={(row) => (
            <LookUpTargetPopulationTableRowSurveys
              radioChangeHandler={enableRadioButton && handleRadioChange}
              selectedTargetPopulation={selectedTargetPopulation}
              key={row.id}
              targetPopulation={row}
              canViewDetails={canViewDetails}
            />
          )}
        />
      </TableWrapper>
    );
  };
  return noTableStyling ? (
    <NoTableStyling>{renderTable()}</NoTableStyling>
  ) : (
    renderTable()
  );
};
