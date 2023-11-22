import { Button } from '@material-ui/core';
import React, { ReactElement, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  AllProgramsForChoicesDocument,
  useCreateProgramMutation,
} from '../../../__generated__/graphql';
import { ALL_PROGRAMS_QUERY } from '../../../apollo/queries/program/AllPrograms';
import { LoadingButton } from '../../../components/core/LoadingButton';
import { useBaseUrl } from '../../../hooks/useBaseUrl';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { ProgramForm } from '../../forms/ProgramForm';
import { PageHeader } from '../../../components/core/PageHeader';
import { BaseSection } from '../../../components/core/BaseSection';
import { ProgramPartnersSection } from '../../../components/programs/CreateProgram/ProgramPartnersSection';

export const CreateProgramPage = (): ReactElement => {
  const [step, setStep] = useState(0);
  const { t } = useTranslation();
  const { showMessage } = useSnackbar();
  const { baseUrl, businessArea } = useBaseUrl();
  const [mutate, { loading }] = useCreateProgramMutation({
    refetchQueries: () => [
      { query: ALL_PROGRAMS_QUERY, variables: { businessArea } },
    ],
  });

  const handleSubmit = async (values): Promise<void> => {
    try {
      const response = await mutate({
        variables: {
          programData: {
            ...values,
            startDate: values.startDate,
            endDate: values.endDate,
            businessAreaSlug: businessArea,
          },
        },
        refetchQueries: () => [
          {
            query: AllProgramsForChoicesDocument,
            variables: { businessArea, first: 100 },
          },
        ],
      });
      showMessage('Programme created.', {
        pathname: `/${baseUrl}/details/${response.data.createProgram.program.id}`,
        historyMethod: 'push',
      });
    } catch (e) {
      e.graphQLErrors.map((x) => showMessage(x.message));
    }
  };

  const renderActions = (submitHandler): ReactElement => {
    return (
      <>
        <Button component={Link} to={`/${baseUrl}/list`}>
          {t('Cancel')}
        </Button>
        <LoadingButton
          loading={loading}
          onClick={submitHandler}
          type='submit'
          color='primary'
          variant='contained'
          data-cy='button-save'
        >
          {t('Save')}
        </LoadingButton>
      </>
    );
  };

  const detailsDescription = t(
    'To create a new Programme, please complete all required fields on the form below and save.',
  );

  return (
    <>
      {step === 0 && (
        <>
          <PageHeader title={t('Create Programme')} />
          <BaseSection title={t('Details')} description={detailsDescription}>
            <>
              <ProgramForm
                actions={(submit) => renderActions(submit)}
                onSubmit={handleSubmit}
              />
            </>
          </BaseSection>
          <ProgramPartnersSection setStep={setStep} />
        </>
      )}
      {step === 1 && (
        <>
          <PageHeader
            title={t('Add Partners')}
            handleBack={() => setStep(0)}
            breadCrumbs={[
              {
                title: t('New Programme'),
                handleClick: () => setStep(0),
              },
            ]}
          />
        </>
      )}
    </>
  );
};
