import { TargetCriteriaForm } from '@containers/forms/TargetCriteriaForm';
import {
  DataCollectingTypeType,
  TargetPopulationQuery,
} from '@generated/graphql';
import { AddCircleOutline } from '@mui/icons-material';
import { Box, Button, Checkbox, FormControlLabel, Grid } from '@mui/material';
import { FormikCheckboxField } from '@shared/Formik/FormikCheckboxField';
import { Field } from 'formik';
import * as React from 'react';
import { Fragment, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { Criteria } from './Criteria';
import { TargetingCriteriaDisabled } from './TargetingCriteriaDisabled';
import {
  ContentWrapper,
  VulnerabilityScoreComponent,
} from './VulnerabilityScoreComponent';

const Title = styled.div`
  padding: ${({ theme }) => theme.spacing(3)} ${({ theme }) => theme.spacing(4)};
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Divider = styled.div`
  border-left: 1px solid #b1b1b5;
  margin: 0 ${({ theme }) => theme.spacing(10)};
  position: relative;
  transform: scale(0.9);
`;

const DividerLabel = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
  color: #253b46;
  text-transform: uppercase;
  padding: 5px;
  border: 1px solid #b1b1b5;
  border-radius: 50%;
  background-color: #fff;
`;

const AddCriteria = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  color: #003c8f;
  border: 2px solid #033f91;
  border-radius: 3px;
  font-size: 16px;
  padding: ${({ theme }) => theme.spacing(6)}
    ${({ theme }) => theme.spacing(28)};
  cursor: pointer;
  p {
    font-weight: 500;
    margin: 0 0 0 ${({ theme }) => theme.spacing(2)};
  }
`;

interface TargetingCriteriaProps {
  rules?;
  helpers?;
  targetPopulation?: TargetPopulationQuery['targetPopulation'];
  selectedProgram?;
  isEdit?: boolean;
  screenBeneficiary: boolean;
  isSocialDctType: boolean;
  isStandardDctType: boolean;
  category: string;
}

export const TargetingCriteria = ({
  rules,
  helpers,
  targetPopulation,
  selectedProgram,
  isEdit,
  screenBeneficiary,
  isSocialDctType,
  isStandardDctType,
  category,
}: TargetingCriteriaProps): React.ReactElement => {
  const { t } = useTranslation();
  const location = useLocation();
  const [isOpen, setOpen] = useState(false);
  const [criteriaIndex, setIndex] = useState(null);
  const [criteriaObject, setCriteria] = useState({});
  const regex = /(create|edit-tp)/;
  const isDetailsPage = !regex.test(location.pathname);
  const openModal = (criteria): void => {
    setCriteria(criteria);
    setOpen(true);
  };
  const closeModal = (): void => {
    setCriteria({});
    setIndex(null);
    return setOpen(false);
  };
  const editCriteria = (criteria, index): void => {
    setIndex(index);
    return openModal(criteria);
  };

  const addCriteria = (values): void => {
    const criteria = {
      filters: [...values.filters],
      individualsFiltersBlocks: [...values.individualsFiltersBlocks],
    };
    if (criteriaIndex !== null) {
      helpers.replace(criteriaIndex, criteria);
    } else {
      helpers.push(criteria);
    }
    return closeModal();
  };

  let individualFiltersAvailable = true;
  let householdFiltersAvailable = true;

  if (selectedProgram) {
    const { dataCollectingType } = selectedProgram;
    individualFiltersAvailable = dataCollectingType?.individualFiltersAvailable;
    householdFiltersAvailable = dataCollectingType?.householdFiltersAvailable;

    // Allow use filters on non-migrated programs
    if (individualFiltersAvailable === undefined) {
      individualFiltersAvailable = true;
    }
    if (householdFiltersAvailable === undefined) {
      householdFiltersAvailable = true;
    }

    // Disable household filters for social programs
    if (isSocialDctType) {
      householdFiltersAvailable = false;
    }
  }

  if (householdFiltersAvailable || individualFiltersAvailable) {
    return (
      <Box display="flex" flexDirection="column">
        <Title>
          <div />
          {isEdit && (
            <>
              {!!rules.length && category === 'filters' && (
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => setOpen(true)}
                  data-cy="button-target-population-add-criteria"
                >
                  {t('Add')} &apos;Or&apos;
                  {t('Filter')}
                </Button>
              )}
            </>
          )}
        </Title>
        <TargetCriteriaForm
          criteria={criteriaObject}
          open={isOpen}
          onClose={() => closeModal()}
          addCriteria={addCriteria}
          individualFiltersAvailable={individualFiltersAvailable}
          householdFiltersAvailable={householdFiltersAvailable}
        />
        <ContentWrapper>
          <Box display="flex" flexDirection="column">
            <Box display="flex" flexWrap="wrap">
              {rules.length
                ? rules.map((criteria, index) => (
                    // eslint-disable-next-line
                    <Fragment key={criteria.id || index}>
                      <Criteria
                        isEdit={isEdit}
                        canRemove={rules.length > 1}
                        rules={criteria.filters}
                        individualsFiltersBlocks={
                          criteria.individualsFiltersBlocks || []
                        }
                        editFunction={() => editCriteria(criteria, index)}
                        removeFunction={() => helpers.remove(index)}
                      />

                      {index === rules.length - 1 ||
                      (rules.length === 1 && index === 0) ? null : (
                        <Divider>
                          <DividerLabel>Or</DividerLabel>
                        </Divider>
                      )}
                    </Fragment>
                  ))
                : null}

              {category === 'filters' && !rules.length && (
                <AddCriteria
                  onClick={() => setOpen(true)}
                  data-cy="button-target-population-add-criteria"
                >
                  <AddCircleOutline />
                  <p>{t('Add Filter')}</p>
                </AddCriteria>
              )}
            </Box>
            <Box>
              {isDetailsPage ? (
                <Box mt={3} p={3}>
                  <Grid container spacing={3}>
                    <Grid item xs={6}>
                      {isStandardDctType && (
                        <FormControlLabel
                          disabled
                          control={
                            <Checkbox
                              color="primary"
                              name="flagExcludeIfActiveAdjudicationTicket"
                              data-cy="checkbox-exclude-if-active-adjudication-ticket"
                              checked={Boolean(
                                targetPopulation?.targetingCriteria
                                  ?.flagExcludeIfActiveAdjudicationTicket,
                              )}
                            />
                          }
                          label={t(
                            'Exclude Households with Active Adjudication Ticket',
                          )}
                        />
                      )}
                      {isSocialDctType && (
                        <FormControlLabel
                          disabled
                          control={
                            <Checkbox
                              color="primary"
                              name="flagExcludeIfActiveAdjudicationTicket"
                              data-cy="checkbox-exclude-people-if-active-adjudication-ticket"
                              checked={Boolean(
                                targetPopulation?.targetingCriteria
                                  ?.flagExcludeIfActiveAdjudicationTicket,
                              )}
                            />
                          }
                          label={t(
                            'Exclude People with Active Adjudication Ticket',
                          )}
                        />
                      )}
                    </Grid>
                    <Grid item xs={6}>
                      {screenBeneficiary && (
                        <FormControlLabel
                          disabled
                          control={
                            <Checkbox
                              data-cy="checkbox-exclude-if-on-sanction-list"
                              color="primary"
                              name="flagExcludeIfOnSanctionList"
                            />
                          }
                          checked={Boolean(
                            targetPopulation?.targetingCriteria
                              ?.flagExcludeIfOnSanctionList,
                          )}
                          label={t(
                            'Exclude Households with an active sanction screen flag',
                          )}
                        />
                      )}
                    </Grid>
                  </Grid>
                </Box>
              ) : (
                <Box mt={3} p={3}>
                  <Grid container spacing={3}>
                    {isStandardDctType && (
                      <Grid item xs={6}>
                        <Field
                          name="flagExcludeIfActiveAdjudicationTicket"
                          label={t(
                            'Exclude Households with Active Adjudication Ticket',
                          )}
                          color="primary"
                          component={FormikCheckboxField}
                          data-cy="input-active-adjudication-ticket"
                        />
                      </Grid>
                    )}
                    {isSocialDctType && (
                      <Grid item xs={6}>
                        <Field
                          name="flagExcludePeopleWithActiveAdjudicationTicket"
                          label={t(
                            'Exclude People with Active Adjudication Ticket',
                          )}
                          color="primary"
                          component={FormikCheckboxField}
                          data-cy="input-active-adjudication-ticket"
                        />
                      </Grid>
                    )}
                    {screenBeneficiary && (
                      <Grid item xs={6}>
                        <Field
                          name="flagExcludeIfOnSanctionList"
                          label={t(
                            'Exclude Households with an active sanction screen flag',
                          )}
                          color="primary"
                          component={FormikCheckboxField}
                          data-cy="input-active-sanction-flag"
                        />
                      </Grid>
                    )}
                  </Grid>
                </Box>
              )}
            </Box>
          </Box>
        </ContentWrapper>
        {targetPopulation && (
          <VulnerabilityScoreComponent targetPopulation={targetPopulation} />
        )}
      </Box>
    );
  }
  return <TargetingCriteriaDisabled showTooltip />;
};
