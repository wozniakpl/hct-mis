import { Button, Grid, MenuItem, Paper } from '@material-ui/core';
import FlashOnIcon from '@material-ui/icons/FlashOn';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { useAllProgramsForChoicesQuery } from '../../__generated__/graphql';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { createHandleApplyFilterChange } from '../../utils/utils';
import { LoadingComponent } from '../core/LoadingComponent';
import { SelectFilter } from '../core/SelectFilter';
import { AdminAreaAutocomplete } from '../population/AdminAreaAutocomplete';

const Container = styled(Paper)`
  display: flex;
  flex-direction: column;
  flex: 1;
  width: 100%;
  background-color: #fff;
  padding: ${({ theme }) => theme.spacing(8)}px
    ${({ theme }) => theme.spacing(11)}px;
  align-items: center;
  && > div {
    margin: 5px;
  }
`;

interface DashboardFiltersProps {
  onFilterChange;
  filter;
  setFilter;
  initialFilter;
  appliedFilter;
  setAppliedFilter;
}

export const DashboardFilters = ({
  onFilterChange,
  filter,
  setFilter,
  initialFilter,
  appliedFilter,
  setAppliedFilter,
}: DashboardFiltersProps): React.ReactElement => {
  const { t } = useTranslation();
  const businessArea = useBusinessArea();
  const history = useHistory();
  const location = useLocation();
  const { data, loading } = useAllProgramsForChoicesQuery({
    variables: { businessArea },
    fetchPolicy: 'cache-and-network',
  });
  if (loading) return <LoadingComponent />;

  const allPrograms = data?.allPrograms?.edges || [];
  const programs = allPrograms.map((edge) => edge.node);

  const {
    handleFilterChange,
    applyFilterChanges,
    clearFilter,
  } = createHandleApplyFilterChange(
    onFilterChange,
    initialFilter,
    history,
    location,
    filter,
    setFilter,
    appliedFilter,
    setAppliedFilter,
  );
  const handleApplyFilter = (): void => {
    applyFilterChanges();
  };

  const handleClearFilter = (): void => {
    clearFilter();
  };

  return (
    <Container>
      <Grid container alignItems='flex-end' spacing={3}>
        <Grid item xs={5}>
          <SelectFilter
            onChange={(e) => handleFilterChange('program', e.target.value)}
            label={t('Programme')}
            value={filter.program}
            icon={<FlashOnIcon />}
            fullWidth
          >
            <MenuItem value=''>
              <em>None</em>
            </MenuItem>
            {programs.map((program) => (
              <MenuItem key={program.id} value={program.id}>
                {program.name}
              </MenuItem>
            ))}
          </SelectFilter>
        </Grid>
        <Grid item xs={3}>
          <AdminAreaAutocomplete
            fullWidth
            name='administrativeArea'
            value={filter.administrativeArea}
            onFilterChange={onFilterChange}
            filter={filter}
          />
        </Grid>
      </Grid>
      <Grid container justifyContent='flex-end'>
        <Button
          color='primary'
          onClick={() => {
            handleClearFilter();
          }}
        >
          {t('Clear')}
        </Button>
        <Button
          color='primary'
          variant='outlined'
          onClick={() => handleApplyFilter()}
        >
          {t('Apply')}
        </Button>
      </Grid>
    </Container>
  );
};
