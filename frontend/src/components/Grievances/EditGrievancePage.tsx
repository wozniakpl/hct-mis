import React from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';
import { Field, Formik } from 'formik';
import { Box, Button, DialogActions, Grid } from '@material-ui/core';
import camelCase from 'lodash/camelCase';
import { FormikTextField } from '../../shared/Formik/FormikTextField';
import { PageHeader } from '../PageHeader';
import { BreadCrumbsItem } from '../BreadCrumbs';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { ContainerColumnWithBorder } from '../ContainerColumnWithBorder';
import { FormikSelectField } from '../../shared/Formik/FormikSelectField';
import { FormikCheckboxField } from '../../shared/Formik/FormikCheckboxField';
import {
  GrievanceTicketDocument,
  GrievanceTicketQuery,
  useAllUsersQuery,
  useCreateGrievanceMutation,
  useGrievancesChoiceDataQuery,
  useGrievanceTicketQuery,
  useUpdateGrievanceMutation,
} from '../../__generated__/graphql';
import { LoadingComponent } from '../LoadingComponent';
import { useSnackbar } from '../../hooks/useSnackBar';
import { FormikAdminAreaAutocomplete } from '../../shared/Formik/FormikAdminAreaAutocomplete';
import {
  GRIEVANCE_CATEGORIES,
  GRIEVANCE_ISSUE_TYPES,
} from '../../utils/constants';
import {
  decodeIdString,
  renderUserName,
  thingForSpecificGrievanceType,
} from '../../utils/utils';
import { Consent } from './Consent';
import { LookUpSection } from './LookUpSection';
import { OtherRelatedTicketsCreate } from './OtherRelatedTicketsCreate';
import { AddIndividualDataChange } from './AddIndividualDataChange';
import { EditIndividualDataChange } from './EditIndividualDataChange';
import { EditHouseholdDataChange } from './EditHouseholdDataChange';
import {
  dataChangeComponentDict,
  EmptyComponent,
  prepareInitialValues,
  prepareVariables,
  validationSchema,
} from './utils/editGrievanceUtils';

const BoxPadding = styled.div`
  padding: 15px 0;
`;
const NewTicket = styled.div`
  padding: 20px;
`;
const DialogFooter = styled.div`
  padding: 12px 16px;
  margin: 0;
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  text-align: right;
`;
const BoxWithBorderBottom = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  padding: 15px 0;
`;
const BoxWithBorders = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  padding: 15px 0;
`;

export function EditGrievancePage(): React.ReactElement {
  const businessArea = useBusinessArea();
  const { showMessage } = useSnackbar();
  const { id } = useParams();

  const { data: ticketData, loading: ticketLoading } = useGrievanceTicketQuery({
    variables: {
      id,
    },
  });

  const { data: userData, loading: userDataLoading } = useAllUsersQuery({
    variables: { businessArea },
  });

  const {
    data: choicesData,
    loading: choicesLoading,
  } = useGrievancesChoiceDataQuery();

  const [mutate] = useUpdateGrievanceMutation();

  if (userDataLoading || choicesLoading || ticketLoading) {
    return <LoadingComponent />;
  }
  if (!choicesData || !userData || !ticketData) return null;

  const ticket = ticketData?.grievanceTicket;
  const mappedLinkedTickets = ticketData?.grievanceTicket?.relatedTickets?.map(
    (edge) => edge.id,
  );

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const initialValues: any = prepareInitialValues(ticket);

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: 'Grievance and Feedback',
      to: `/${businessArea}/grievance-and-feedback/${ticket.id}`,
    },
  ];

  const mappedIndividuals = userData.allUsers.edges.map((edge) => ({
    name: renderUserName(edge.node),
    value: edge.node.id,
  }));

  const issueTypeDict = choicesData.grievanceTicketIssueTypeChoices.reduce(
    (prev, curr) => {
      // eslint-disable-next-line no-param-reassign
      prev[curr.category] = curr;
      return prev;
    },
    {},
  );

  return (
    <Formik
      initialValues={initialValues}
      onSubmit={async (values) => {
        try {
          const { variables } = prepareVariables(businessArea, values, ticket);
          await mutate({
            variables,
            refetchQueries: () => [
              {
                query: GrievanceTicketDocument,
                variables: { id: ticket.id },
              },
            ],
          }).then((res) => {
            return showMessage('Grievance Ticket created.', {
              pathname: `/${businessArea}/grievance-and-feedback/${res.data.updateGrievanceTicket.grievanceTicket.id}`,
              historyMethod: 'push',
            });
          });
        } catch (e) {
          e.graphQLErrors.map((x) => showMessage(x.message));
        }
      }}
      validationSchema={validationSchema}
    >
      {({ submitForm, values, setFieldValue }) => {
        const DatachangeComponent = thingForSpecificGrievanceType(
          values,
          dataChangeComponentDict,
          EmptyComponent,
        );
        return (
          <>
            <PageHeader
              title={`Edit Ticket #${decodeIdString(id)}`}
              breadCrumbs={breadCrumbsItems}
            />
            <Grid container spacing={3}>
              <Grid item xs={8}>
                <NewTicket>
                  <ContainerColumnWithBorder>
                    <Grid container spacing={3}>
                      <Grid item xs={6}>
                        <Field
                          name='category'
                          label='Category*'
                          disabled
                          onChange={(e) => {
                            setFieldValue('category', e.target.value);
                            setFieldValue('issueType', null);
                          }}
                          variant='outlined'
                          choices={
                            choicesData.grievanceTicketManualCategoryChoices
                          }
                          component={FormikSelectField}
                        />
                      </Grid>
                      {values.category.toString() ===
                        GRIEVANCE_CATEGORIES.SENSITIVE_GRIEVANCE ||
                      values.category.toString() ===
                        GRIEVANCE_CATEGORIES.DATA_CHANGE ? (
                        <Grid item xs={6}>
                          <Field
                            name='issueType'
                            disabled
                            label='Issue Type*'
                            variant='outlined'
                            choices={
                              issueTypeDict[values.category.toString()]
                                .subCategories
                            }
                            component={FormikSelectField}
                          />
                        </Grid>
                      ) : null}
                    </Grid>
                    <BoxWithBorders>
                      <Box display='flex' flexDirection='column'>
                        <Consent />
                        <Field
                          name='consent'
                          label='Received Consent*'
                          color='primary'
                          disabled
                          component={FormikCheckboxField}
                        />
                        <LookUpSection
                          values={values}
                          disabledHouseholdIndividual
                          disabledPaymentRecords
                          onValueChange={setFieldValue}
                        />
                      </Box>
                    </BoxWithBorders>
                    <BoxWithBorderBottom>
                      <Grid container spacing={3}>
                        <Grid item xs={6}>
                          <Field
                            name='assignedTo'
                            label='Assigned to*'
                            variant='outlined'
                            choices={mappedIndividuals}
                            component={FormikSelectField}
                          />
                        </Grid>
                      </Grid>
                    </BoxWithBorderBottom>
                    <BoxPadding>
                      <Grid container spacing={3}>
                        <Grid item xs={12}>
                          <Field
                            name='description'
                            multiline
                            fullWidth
                            disabled={ticket.description}
                            variant='outlined'
                            label='Description*'
                            component={FormikTextField}
                          />
                        </Grid>
                        <Grid item xs={6}>
                          <Field
                            name='admin'
                            label='Administrative Level 2'
                            disabled={ticket.admin}
                            variant='outlined'
                            component={FormikAdminAreaAutocomplete}
                          />
                        </Grid>
                        <Grid item xs={6}>
                          <Field
                            name='area'
                            fullWidth
                            disabled={ticket.area}
                            variant='outlined'
                            label='Area / Village / Pay point'
                            component={FormikTextField}
                          />
                        </Grid>
                        <Grid item xs={6}>
                          <Field
                            name='language'
                            multiline
                            fullWidth
                            disabled={ticket.language}
                            variant='outlined'
                            label='Languages Spoken*'
                            component={FormikTextField}
                          />
                        </Grid>
                      </Grid>
                    </BoxPadding>
                    <BoxPadding>
                      <DatachangeComponent
                        values={values}
                        setFieldValue={setFieldValue}
                      />
                    </BoxPadding>

                    <DialogFooter>
                      <DialogActions>
                        <Button
                          component={Link}
                          to={`/${businessArea}/grievance-and-feedback`}
                        >
                          Cancel
                        </Button>
                        <Button
                          color='primary'
                          variant='contained'
                          onClick={submitForm}
                        >
                          Save
                        </Button>
                      </DialogActions>
                    </DialogFooter>
                  </ContainerColumnWithBorder>
                </NewTicket>
              </Grid>
              <Grid item xs={4}>
                <NewTicket>
                  {values.category && values.selectedHousehold?.id ? (
                    <OtherRelatedTicketsCreate values={values} />
                  ) : null}
                </NewTicket>
              </Grid>
            </Grid>
          </>
        );
      }}
    </Formik>
  );
}
