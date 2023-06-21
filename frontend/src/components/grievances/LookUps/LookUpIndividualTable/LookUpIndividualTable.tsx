import React, { useEffect } from 'react';
import styled from 'styled-components';
import {
  AllIndividualsQuery,
  AllIndividualsQueryVariables,
  useAllIndividualsQuery,
  useHouseholdLazyQuery,
} from '../../../../__generated__/graphql';
import { UniversalTable } from '../../../../containers/tables/UniversalTable';
import { useBaseUrl } from '../../../../hooks/useBaseUrl';
import { decodeIdString } from '../../../../utils/utils';
import { TableWrapper } from '../../../core/TableWrapper';
import { headCells } from './LookUpIndividualTableHeadCells';
import { LookUpIndividualTableRow } from './LookUpIndividualTableRow';

interface LookUpIndividualTableProps {
  filter;
  businessArea?: string;
  setFieldValue;
  valuesInner;
  selectedIndividual;
  selectedHousehold;
  setSelectedIndividual;
  setSelectedHousehold;
  ticket?;
  excludedId?;
  noTableStyling?;
}

const NoTableStyling = styled.div`
  .MuiPaper-elevation1 {
    box-shadow: none;
    padding: 0 !important;
  }
`;

export const LookUpIndividualTable = ({
  businessArea,
  filter,
  setFieldValue,
  valuesInner,
  selectedIndividual,
  setSelectedIndividual,
  setSelectedHousehold,
  ticket,
  excludedId,
  noTableStyling = false,
}: LookUpIndividualTableProps): React.ReactElement => {
  const [getHousehold, results] = useHouseholdLazyQuery();
  const { programId } = useBaseUrl();
  useEffect(() => {
    if (results.data && !results.loading && !results.error) {
      setFieldValue('selectedHousehold', results.data.household);
      setSelectedHousehold(results.data.household);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [results, setSelectedHousehold]);

  const handleRadioChange = (individual): void => {
    if (individual.household?.id) {
      getHousehold({ variables: { id: individual.household.id.toString() } });
    }
    setSelectedIndividual(individual);
    setFieldValue('selectedIndividual', individual);
    setFieldValue('identityVerified', false);
  };
  let householdId;
  if ('household' in filter) {
    householdId = decodeIdString(filter.household);
  } else {
    householdId = valuesInner.selectedHousehold
      ? decodeIdString(valuesInner.selectedHousehold.id)
      : null;
  }

  const initialVariables: AllIndividualsQueryVariables = {
    businessArea,
    search: filter.search,
    admin2: [decodeIdString(filter?.admin2?.node?.id)],
    sex: [filter.sex],
    age: JSON.stringify({ min: filter.ageMin, max: filter.ageMax }),
    flags: [],
    programs: [decodeIdString(programId)],
    lastRegistrationDate: JSON.stringify({
      min: filter.lastRegistrationDateMin,
      max: filter.lastRegistrationDateMax,
    }),
    status: filter.status,
    orderBy: filter.orderBy,
    householdId,
    excludedId: excludedId || ticket?.individual?.id || null,
  };

  const renderTable = (): React.ReactElement => {
    return (
      <UniversalTable<
        AllIndividualsQuery['allIndividuals']['edges'][number]['node'],
        AllIndividualsQueryVariables
      >
        headCells={headCells}
        rowsPerPageOptions={[5, 10, 15, 20]}
        query={useAllIndividualsQuery}
        queriedObjectName='allIndividuals'
        initialVariables={initialVariables}
        renderRow={(row) => (
          <LookUpIndividualTableRow
            radioChangeHandler={handleRadioChange}
            selectedIndividual={selectedIndividual}
            key={row.id}
            individual={row}
          />
        )}
      />
    );
  };
  return noTableStyling ? (
    <NoTableStyling>{renderTable()}</NoTableStyling>
  ) : (
    <TableWrapper>{renderTable()}</TableWrapper>
  );
};
