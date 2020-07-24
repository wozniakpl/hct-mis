import React, { useState } from 'react';
import { Formik, Form, Field } from 'formik';
import styled from 'styled-components';
import {
  Button,
  DialogContent,
  DialogTitle,
  Tabs,
  Tab,
  Typography,
  Box,
} from '@material-ui/core';
import CheckRoundedIcon from '@material-ui/icons/CheckRounded';

import { useSnackbar } from '../../hooks/useSnackBar';
import { Dialog } from '../../containers/dialogs/Dialog';
import { DialogActions } from '../../containers/dialogs/DialogActions';
import { TabPanel } from '../TabPanel';
import { FormikSliderField } from '../../shared/Formik/FormikSliderField';
import { FormikCheckboxField } from '../../shared/Formik/FormikCheckboxField';
import { FormikRadioGroup } from '../../shared/Formik/FormikRadioGroup';
import {
  useCreateCashPlanPaymentVerificationMutation,
  AllAdminAreasQuery,
  useAllAdminAreasQuery,
} from '../../__generated__/graphql';
import { FormikMultiSelectField } from '../../shared/Formik/FormikMultiSelectField';
import { AdminAreasAutocomplete } from '../population/AdminAreaAutocomplete';
import { useBusinessArea } from '../../hooks/useBusinessArea';

const DialogTitleWrapper = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
`;

const DialogFooter = styled.div`
  padding: 12px 16px;
  margin: 0;
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  text-align: right;
`;

const StyledTabs = styled(Tabs)`
  && {
    max-width: 500px;
  }
`;
const TabsContainer = styled.div`
  border-bottom: 1px solid #e8e8e8;
`;
const DialogContainer = styled.div`
  width: 700px;
`;

export function NewPaymentVerificationDialog(): React.ReactElement {
  const [open, setOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState(0);
  const { showMessage } = useSnackbar();
  const [mutate] = useCreateCashPlanPaymentVerificationMutation();
  const businessArea = useBusinessArea();

  const { data, loading } = useAllAdminAreasQuery({
    variables: {
      first: 100,
      // title: debouncedInputText,
      businessArea,
    },
  });

  const submit = async (values): Promise<void> => {
    const { errors } = await mutate({
      variables: {
        input: {
          cashPlanId:
            'Q2FzaFBsYW5Ob2RlOmFlYmJhMzE5LTkzMmItNGI3MC04OThjLWRmOGIyMTM3ODU4Yw==',
          sampling: 'FULL',
          fullListArguments: {
            excludedAdminAreas: [],
          },
          verificationChannel: 'RAPIDPRO',
          rapidProArguments: {
            flowId: '1',
          },
          businessAreaSlug: 'afghanistan',
        },
      },
    });

    if (errors) {
      showMessage('Error while submitting');
      return;
    }
    showMessage('New verification plan created.');
  };

  const mappedAdminAreas =
    data && data.allAdminAreas.edges.length
      ? data.allAdminAreas.edges.map((el) => ({
          value: el.node.id,
          name: el.node.title,
        }))
      : [];
  const initialValues = {
    confidenceInterval: 8,
    marginOfError: 24,
    admin: false,
    age: true,
    sex: false,
    filterAdminAreas: [],
    verificationChannel: null,
  };

  return (
    <Formik initialValues={initialValues} onSubmit={submit}>
      {({ submitForm, values }) => (
        <Form>
          <Button
            color='primary'
            variant='contained'
            onClick={() => setOpen(true)}
            data-cy='button-new-plan'
          >
            CREATE VERIFICATION PLAN
          </Button>
          <Dialog
            open={open}
            onClose={() => setOpen(false)}
            scroll='paper'
            aria-labelledby='form-dialog-title'
          >
            <DialogTitleWrapper>
              <DialogTitle id='scroll-dialog-title'>
                Create Verification Plan
              </DialogTitle>
            </DialogTitleWrapper>
            <DialogContent>
              <DialogContainer>
                <TabsContainer>
                  <StyledTabs
                    value={selectedTab}
                    onChange={(
                      event: React.ChangeEvent<{}>,
                      newValue: number,
                    ) => setSelectedTab(newValue)}
                    indicatorColor='primary'
                    textColor='primary'
                    variant='fullWidth'
                    aria-label='full width tabs example'
                  >
                    <Tab label='FULL LIST' />
                    <Tab label='RANDOM SAMPLING' />
                  </StyledTabs>
                </TabsContainer>
                <TabPanel value={selectedTab} index={0}>
                  <Field
                    name='filterAdminAreas'
                    choices={mappedAdminAreas}
                    variant='filled'
                    label='Filter Out Admin Areas'
                    component={FormikMultiSelectField}
                  />
                  <Box pt={3}>
                    <Box
                      pb={3}
                      pt={3}
                      fontSize={16}
                      fontWeight='fontWeightBold'
                    >
                      Sample size: 500 out of 500 (100%)
                    </Box>
                    <Field
                      name='verificationChannel'
                      label='Verification Channel'
                      style={{ flexDirection: 'row' }}
                      choices={[
                        { value: 'RAPIDPRO', name: 'RAPIDPRO' },
                        { value: 'XLSX', name: 'XLSX' },
                        { value: 'MANUAL', name: 'MANUAL' },
                      ]}
                      component={FormikRadioGroup}
                    />
                  </Box>
                </TabPanel>
                <TabPanel value={selectedTab} index={1}>
                  <Box pt={3}>
                    <Field
                      name='confidenceInterval'
                      label='Confidence Interval'
                      component={FormikSliderField}
                    />
                    <Field
                      name='marginOfError'
                      label='Margin of Error'
                      component={FormikSliderField}
                    />
                    <Typography variant='caption'>Cluster Filters</Typography>
                    <Box display='flex'>
                      <Field
                        name='admin'
                        label='Admin'
                        color='primary'
                        component={FormikCheckboxField}
                      />
                      <Field
                        name='age'
                        label='Age'
                        color='primary'
                        component={FormikCheckboxField}
                      />
                      <Field
                        name='sex'
                        label='Sex'
                        color='primary'
                        component={FormikCheckboxField}
                      />
                    </Box>
                    <Field
                      name='filterAdminAreas'
                      choices={mappedAdminAreas}
                      variant='filled'
                      label='Filter Out Admin Areas'
                      component={FormikMultiSelectField}
                    />
                    <Box
                      pb={3}
                      pt={3}
                      fontSize={16}
                      fontWeight='fontWeightBold'
                    >
                      Sample size: 435 out of 500 ({(435 / 500) * 100}%)
                    </Box>
                    <Field
                      name='verificationChannel'
                      label='Verification Channel'
                      style={{ flexDirection: 'row' }}
                      choices={[
                        { value: 'RAPIDPRO', name: 'RAPIDPRO' },
                        { value: 'XLSX', name: 'XLSX' },
                        { value: 'MANUAL', name: 'MANUAL' },
                      ]}
                      component={FormikRadioGroup}
                    />
                  </Box>
                </TabPanel>
              </DialogContainer>
            </DialogContent>
            <DialogFooter>
              <DialogActions>
                <Button onClick={() => setOpen(false)}>CANCEL</Button>
                <Button
                  startIcon={<CheckRoundedIcon />}
                  type='submit'
                  color='primary'
                  variant='contained'
                  onClick={submitForm}
                  data-cy='button-submit'
                >
                  SAVE
                </Button>
              </DialogActions>
            </DialogFooter>
          </Dialog>
        </Form>
      )}
    </Formik>
  );
}
