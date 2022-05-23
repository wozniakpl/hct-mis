import { Box, Button } from '@material-ui/core';
import { Link, useParams } from 'react-router-dom';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { hasPermissions, PERMISSIONS } from '../../../../config/permissions';
import { BreadCrumbsItem } from '../../../core/BreadCrumbs';
import { PageHeader } from '../../../core/PageHeader';

interface EditFspHeaderProps {
  handleSubmit: () => Promise<void>;
  businessArea: string;
  permissions: string[];
}

export function EditSetUpFspHeader({
  handleSubmit,
  businessArea,
  permissions,
}: EditFspHeaderProps): React.ReactElement {
  const { t } = useTranslation();
  const { id } = useParams();

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: t('Payment Module'),
      to: `/${businessArea}/payment-module/`,
    },
  ];

  return (
    <PageHeader
      title={t('Set up FSP')}
      breadCrumbs={
        hasPermissions(PERMISSIONS.PAYMENT_MODULE_VIEW_LIST, permissions)
          ? breadCrumbsItems
          : null
      }
    >
      <Box display='flex' mt={2} mb={2}>
        <Box mr={3}>
          <Button
            component={Link}
            to={`/${businessArea}/payment-module/payment-plan/${id}/setup-fsp`}
          >
            {t('Cancel')}
          </Button>
        </Box>
        <Button variant='contained' color='primary' onClick={handleSubmit}>
          {t('Save')}
        </Button>
      </Box>
    </PageHeader>
  );
}
