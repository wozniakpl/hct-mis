import React, { useState, useRef } from 'react';
import styled from 'styled-components';
import { useTranslation } from 'react-i18next';
import { Button } from '@material-ui/core';
import { debounce } from 'lodash';
import { PageHeader } from '../../components/PageHeader';
import { TargetPopulationFilters } from '../../components/TargetPopulation/TargetPopulationFilters';
import { TargetPopulationTable } from '../TargetPopulationTable';

const Container = styled.div`
  && {
    display: flex;
    flex-direction: column;
    min-width: 100%;
  }
`;

const TableWrapper = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding: 20px;
  padding-bottom: 0;
`;

export function TargetPopulationPage() {
  const { t } = useTranslation();
  const [sizeFilter, setSizeFilter] = useState({
    min: undefined,
    max: undefined,
  });
  //TODO: create a hook to handle those
  const [textFilter, setTextFilter] = useState('');
  const handleMinSizeFilter = (value: number): void => {
    setSizeFilter({ ...sizeFilter, min: value });
  };
  const handleMaxSizeFilter = (value: number): void => {
    if (value < sizeFilter.min) {
      setSizeFilter({ ...sizeFilter, min: sizeFilter.min + 1 });
    } else {
      setSizeFilter({ ...sizeFilter, max: value });
    }
  };

  const handleTextFilter = useRef(
    debounce((value) => setTextFilter(value), 300),
  ).current;

  return (
    <div>
      <PageHeader title={t('Target Population')}>
        <Button variant='contained' color='primary'>
          Create new
        </Button>
      </PageHeader>
      <TargetPopulationFilters
        minValue={sizeFilter.min}
        maxValue={sizeFilter.max}
        householdMaxSizeFilter={handleMaxSizeFilter}
        householdMinSizeFilter={handleMinSizeFilter}
        householdTextFilter={handleTextFilter}
      />
      <Container>
        <TableWrapper>
          <TargetPopulationTable />
        </TableWrapper>
      </Container>
    </div>
  );
}
