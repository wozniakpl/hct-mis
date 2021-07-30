import {
  Box,
  Button,
  DialogActions,
  FormHelperText,
  Grid,
} from '@material-ui/core';
import { Field, Formik } from 'formik';
import React, { ReactElement } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useHistory } from 'react-router-dom';
import styled from 'styled-components';
import {
  hasPermissionInModule,
  hasPermissions,
  PERMISSIONS,
} from '../../config/permissions';
import { useArrayToDict } from '../../hooks/useArrayToDict';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { usePermissions } from '../../hooks/usePermissions';
import { useSnackbar } from '../../hooks/useSnackBar';
import { FormikAdminAreaAutocomplete } from '../../shared/Formik/FormikAdminAreaAutocomplete';
import { FormikCheckboxField } from '../../shared/Formik/FormikCheckboxField';
import { FormikSelectField } from '../../shared/Formik/FormikSelectField';
import { FormikTextField } from '../../shared/Formik/FormikTextField';
import {
  GRIEVANCE_CATEGORIES,
  GRIEVANCE_ISSUE_TYPES,
} from '../../utils/constants';
import {
  isInvalid,
  renderUserName,
  thingForSpecificGrievanceType,
} from '../../utils/utils';
import {
  useAllAddIndividualFieldsQuery,
  useAllEditHouseholdFieldsQuery,
  useAllUsersQuery,
  useCreateGrievanceMutation,
  useGrievancesChoiceDataQuery,
} from '../../__generated__/graphql';
import { BreadCrumbsItem } from '../BreadCrumbs';
import { ContainerColumnWithBorder } from '../ContainerColumnWithBorder';
import { LoadingComponent } from '../LoadingComponent';
import { PageHeader } from '../PageHeader';
import { PermissionDenied } from '../PermissionDenied';
import { AddIndividualDataChange } from './AddIndividualDataChange';
import { Consent } from './Consent';
import { EditHouseholdDataChange } from './EditHouseholdDataChange';
import { EditIndividualDataChange } from './EditIndividualDataChange';
import { LookUpSection } from './LookUpSection';
import { OtherRelatedTicketsCreate } from './OtherRelatedTicketsCreate';
import { TicketsAlreadyExist } from './TicketsAlreadyExist';
import { prepareVariables } from './utils/createGrievanceUtils';
import { validate } from './utils/validateGrievance';
import { validationSchema } from './utils/validationSchema';

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
const EmptyComponent = (): React.ReactElement => null;
export const dataChangeComponentDict = {
  [GRIEVANCE_CATEGORIES.DATA_CHANGE]: {
    [GRIEVANCE_ISSUE_TYPES.ADD_INDIVIDUAL]: AddIndividualDataChange,
    [GRIEVANCE_ISSUE_TYPES.EDIT_INDIVIDUAL]: EditIndividualDataChange,
    [GRIEVANCE_ISSUE_TYPES.EDIT_HOUSEHOLD]: EditHouseholdDataChange,
  },
};

export function CreateGrievancePage(): React.ReactElement {
  const { t } = useTranslation();
  const history = useHistory();
  const businessArea = useBusinessArea();
  const permissions = usePermissions();
  const { showMessage } = useSnackbar();

  const linkedTicketId = history.location.state?.linkedTicketId;

  const initialValues = {
    description: '',
    assignedTo: '',
    category: null,
    language: '',
    consent: false,
    admin: null,
    area: '',
    selectedHousehold: null,
    selectedIndividual: null,
    selectedPaymentRecords: [],
    selectedRelatedTickets: linkedTicketId ? [linkedTicketId] : [],
    identityVerified: false,
    issueType: null,
  };
  const { data: userData, loading: userDataLoading } = useAllUsersQuery({
    variables: { businessArea },
  });

  const {
    data: choicesData,
    loading: choicesLoading,
  } = useGrievancesChoiceDataQuery();

  const [mutate] = useCreateGrievanceMutation();
  const {
    data: allAddIndividualFieldsData,
    loading: allAddIndividualFieldsDataLoading,
  } = useAllAddIndividualFieldsQuery();
  const {
    data: householdFieldsData,
    loading: householdFieldsLoading,
  } = useAllEditHouseholdFieldsQuery();
  const individualFieldsDict = useArrayToDict(
    allAddIndividualFieldsData?.allAddIndividualsFieldsAttributes,
    'name',
    '*',
  );
  const householdFieldsDict = useArrayToDict(
    householdFieldsData?.allEditHouseholdFieldsAttributes,
    'name',
    '*',
  );
  const issueTypeDict = useArrayToDict(
    choicesData?.grievanceTicketIssueTypeChoices,
    'category',
    '*',
  );

  if (
    userDataLoading ||
    choicesLoading ||
    allAddIndividualFieldsDataLoading ||
    householdFieldsLoading
  )
    return <LoadingComponent />;
  if (permissions === null) return null;

  if (!hasPermissions(PERMISSIONS.GRIEVANCES_CREATE, permissions))
    return <PermissionDenied />;

  if (
    !choicesData ||
    !userData ||
    !allAddIndividualFieldsData ||
    !householdFieldsData ||
    !householdFieldsDict ||
    !individualFieldsDict
  )
    return null;

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: t('Grievance and Feedback'),
      to: `/${businessArea}/grievance-and-feedback/`,
    },
  ];

  const mappedIndividuals = userData.allUsers.edges.map((edge) => ({
    name: renderUserName(edge.node),
    value: edge.node.id,
  }));

  const dataChangeErrors = (errors, touched): ReactElement[] =>
    [
      'householdDataUpdateFields',
      'individualDataUpdateFields',
      'individualDataUpdateFieldsDocuments',
      'individualDataUpdateFieldsIdentities',
    ].map(
      (fieldname) =>
        isInvalid(fieldname, errors, touched) && (
          <FormHelperText key={fieldname} error>
            {errors[fieldname]}
          </FormHelperText>
        ),
    );

  return (
    <Formik
      initialValues={initialValues}
      onSubmit={async (values) => {
        try {
          const response = await mutate(prepareVariables(businessArea, values));
          if (values.selectedPaymentRecords.length > 1) {
            showMessage(
              `${values.selectedPaymentRecords.length} ${t(
                'Grievance Tickets created',
              )}.`,
              {
                pathname: `/${businessArea}/grievance-and-feedback`,
                historyMethod: 'push',
              },
            );
          } else {
            showMessage(t('Grievance Ticket created.'), {
              pathname: `/${businessArea}/grievance-and-feedback/${response.data.createGrievanceTicket.grievanceTickets[0].id}`,
              historyMethod: 'push',
            });
          }
        } catch (e) {
          e.graphQLErrors.map((x) => showMessage(x.message));
        }
      }}
      validate={(values) =>
        validate(
          values,
          allAddIndividualFieldsData,
          individualFieldsDict,
          householdFieldsDict,
        )
      }
      validationSchema={validationSchema}
    >
      {({ submitForm, values, setFieldValue, errors, touched }) => {
        const DatachangeComponent = thingForSpecificGrievanceType(
          values,
          dataChangeComponentDict,
          EmptyComponent,
        );
        return (
          <>
            <PageHeader
              title='New Ticket'
              breadCrumbs={
                hasPermissionInModule('GRIEVANCES_VIEW_LIST', permissions)
                  ? breadCrumbsItems
                  : null
              }
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
                      {values.category ===
                        GRIEVANCE_CATEGORIES.SENSITIVE_GRIEVANCE ||
                      values.category === GRIEVANCE_CATEGORIES.DATA_CHANGE ? (
                        <Grid item xs={6}>
                          <Field
                            name='issueType'
                            label='Issue Type*'
                            variant='outlined'
                            choices={
                              issueTypeDict[values.category].subCategories
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
                          label={t('Received Consent*')}
                          color='primary'
                          component={FormikCheckboxField}
                        />
                        <LookUpSection
                          values={values}
                          onValueChange={setFieldValue}
                          errors={errors}
                          touched={touched}
                        />
                      </Box>
                    </BoxWithBorders>
                    <BoxWithBorderBottom>
                      <Grid container spacing={3}>
                        <Grid item xs={6}>
                          <Field
                            name='assignedTo'
                            label={t('Assigned to*')}
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
                            variant='outlined'
                            label='Description*'
                            component={FormikTextField}
                          />
                        </Grid>
                        <Grid item xs={6}>
                          <Field
                            name='admin'
                            label={t('Administrative Level 2')}
                            variant='outlined'
                            component={FormikAdminAreaAutocomplete}
                          />
                        </Grid>
                        <Grid item xs={6}>
                          <Field
                            name='area'
                            fullWidth
                            variant='outlined'
                            label={t('Area / Village / Pay point')}
                            component={FormikTextField}
                          />
                        </Grid>
                        <Grid item xs={6}>
                          <Field
                            name='language'
                            multiline
                            fullWidth
                            variant='outlined'
                            label={t('Languages Spoken')}
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
                      {dataChangeErrors(errors, touched)}
                    </BoxPadding>
                    <DialogFooter>
                      <DialogActions>
                        <Button
                          component={Link}
                          to={`/${businessArea}/grievance-and-feedback`}
                        >
                          {t('Cancel')}
                        </Button>
                        <Button
                          color='primary'
                          variant='contained'
                          onClick={submitForm}
                        >
                          {t('Save')}
                        </Button>
                      </DialogActions>
                    </DialogFooter>
                  </ContainerColumnWithBorder>
                </NewTicket>
              </Grid>
              <Grid item xs={4}>
                <NewTicket>
                  {values.category &&
                  values.selectedHousehold?.id &&
                  values.selectedIndividual?.id ? (
                    <TicketsAlreadyExist values={values} />
                  ) : null}
                </NewTicket>
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
