import {
  Box,
  Button,
  Collapse,
  Grid,
  MenuItem,
  Typography,
} from '@material-ui/core';
import { KeyboardArrowDown, KeyboardArrowUp } from '@material-ui/icons';
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { SearchTextField } from '../../../../components/core/SearchTextField';
import { SelectFilter } from '../../../../components/core/SelectFilter';
import { usePaymentVerificationChoicesQuery } from '../../../../__generated__/graphql';

interface VerificationRecordsFiltersProps {
  onFilterChange;
  filter;
  verifications;
}
export function VerificationRecordsFilters({
  onFilterChange,
  filter,
  verifications,
}: VerificationRecordsFiltersProps): React.ReactElement {
  const { t } = useTranslation();
  const [show, setShow] = useState(false);
  const handleFilterChange = (e, name): void =>
    onFilterChange({ ...filter, [name]: e.target.value });
  const { data: choicesData } = usePaymentVerificationChoicesQuery();
  if (!choicesData) {
    return null;
  }

  const verificationPlanOptions = verifications.edges.map((item) => {
    return (
      <MenuItem key={item.node.unicefId} value={item.node.id}>
        {item.node.unicefId}
      </MenuItem>
    );
  });

  return (
    <>
      <Box display='flex' justifyContent='space-between'>
        <Typography variant='h6'>{t('Filters')}</Typography>
        {show ? (
          <Button
            endIcon={<KeyboardArrowUp />}
            color='primary'
            variant='outlined'
            onClick={() => setShow(false)}
            data-cy='button-show'
          >
            {t('HIDE')}
          </Button>
        ) : (
          <Button
            endIcon={<KeyboardArrowDown />}
            color='primary'
            variant='outlined'
            onClick={() => setShow(true)}
            data-cy='button-show'
          >
            {t('SHOW')}
          </Button>
        )}
      </Box>
      <Box>
        <Collapse in={show}>
          <Grid container spacing={3}>
            <Grid item xs={3}>
              <SearchTextField
                value={filter.search}
                label={t('Search')}
                onChange={(e) => handleFilterChange(e, 'search')}
                data-cy='filters-search'
                fullWidth
              />
            </Grid>
            <Grid item xs={3}>
              <SelectFilter
                onChange={(e) => handleFilterChange(e, 'status')}
                label={t('Verification Status')}
                value={filter.status}
                fullWidth
              >
                <MenuItem value=''>
                  <em>None</em>
                </MenuItem>
                {choicesData.paymentVerificationStatusChoices.map((item) => {
                  return (
                    <MenuItem key={item.value} value={item.value}>
                      {item.name}
                    </MenuItem>
                  );
                })}
              </SelectFilter>
            </Grid>
            <Grid item xs={3}>
              <SelectFilter
                onChange={(e) => handleFilterChange(e, 'verificationChannel')}
                label={t('Verification Channel')}
                value={filter.verificationChannel}
              >
                <MenuItem value=''>
                  <em>None</em>
                </MenuItem>
                {choicesData.cashPlanVerificationVerificationChannelChoices.map(
                  (item) => {
                    return (
                      <MenuItem key={item.value} value={item.value}>
                        {item.name}
                      </MenuItem>
                    );
                  },
                )}
              </SelectFilter>
            </Grid>
            <Grid item xs={3}>
              <SelectFilter
                onChange={(e) =>
                  handleFilterChange(e, 'paymentVerificationPlan')
                }
                label={t('Verification Plan Id')}
                value={filter.paymentVerificationPlan}
              >
                <MenuItem value=''>
                  <em>None</em>
                </MenuItem>
                {verificationPlanOptions}
              </SelectFilter>
            </Grid>
          </Grid>
        </Collapse>
      </Box>
    </>
  );
}
