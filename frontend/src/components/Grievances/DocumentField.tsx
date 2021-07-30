import { Grid, IconButton } from '@material-ui/core';
import { Delete } from '@material-ui/icons';
import { Field } from 'formik';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { FormikSelectField } from '../../shared/Formik/FormikSelectField';
import { FormikTextField } from '../../shared/Formik/FormikTextField';
import { AllAddIndividualFieldsQuery } from '../../__generated__/graphql';

export interface DocumentFieldProps {
  index: number;
  baseName: string;
  onDelete: () => {};
  countryChoices: AllAddIndividualFieldsQuery['countriesChoices'];
  documentTypeChoices: AllAddIndividualFieldsQuery['documentTypeChoices'];
}

export function DocumentField({
  index,
  baseName,
  onDelete,
  countryChoices,
  documentTypeChoices,
}: DocumentFieldProps): React.ReactElement {
  const { t } = useTranslation();
  return (
    <>
      <Grid item xs={4}>
        <Field
          name={`${baseName}[${index}].country`}
          fullWidth
          variant='outlined'
          label={t('Country')}
          component={FormikSelectField}
          choices={countryChoices}
          required
        />
      </Grid>
      <Grid item xs={4}>
        <Field
          name={`${baseName}[${index}].type`}
          fullWidth
          variant='outlined'
          label={t('Type')}
          component={FormikSelectField}
          choices={documentTypeChoices}
          required
        />
      </Grid>
      <Grid item xs={3}>
        <Field
          name={`${baseName}[${index}].number`}
          fullWidth
          variant='outlined'
          label={t('Document Number')}
          component={FormikTextField}
          required
        />
      </Grid>
      <Grid item xs={1}>
        <IconButton onClick={onDelete}>
          <Delete />
        </IconButton>
      </Grid>
    </>
  );
}
