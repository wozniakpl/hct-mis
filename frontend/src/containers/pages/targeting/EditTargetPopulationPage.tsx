import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { LoadingComponent } from '../../../components/core/LoadingComponent';
import { PermissionDenied } from '../../../components/core/PermissionDenied';
import { EditTargetPopulation } from '../../../components/targeting/EditTargetPopulation/EditTargetPopulation';
import { usePermissions } from '../../../hooks/usePermissions';
import { isPermissionDeniedError } from '../../../utils/utils';
import {
  TargetPopulationBuildStatus,
  useBusinessAreaDataQuery,
  useTargetPopulationQuery,
} from '../../../__generated__/graphql';
import { useBusinessArea } from '../../../hooks/useBusinessArea';

export const EditTargetPopulationPage = (): React.ReactElement => {
  const { id } = useParams();
  const permissions = usePermissions();
  const {
    data,
    loading,
    error,
    startPolling,
    stopPolling,
  } = useTargetPopulationQuery({
    variables: { id },
    fetchPolicy: 'cache-and-network',
  });
  const businessArea = useBusinessArea();

  const { data: businessAreaData } = useBusinessAreaDataQuery({
    variables: { businessAreaSlug: businessArea },
  });
  const buildStatus = data?.targetPopulation?.buildStatus;
  useEffect(() => {
    if (
      [
        TargetPopulationBuildStatus.Building,
        TargetPopulationBuildStatus.Pending,
      ].includes(buildStatus)
    ) {
      startPolling(3000);
    } else {
      stopPolling();
    }
    return () => stopPolling();
  }, [buildStatus, id, startPolling, stopPolling]);

  if (loading && !data) return <LoadingComponent />;

  if (isPermissionDeniedError(error)) return <PermissionDenied />;

  if (!data || permissions === null || !businessAreaData) return null;

  const { targetPopulation } = data;

  return (
    <EditTargetPopulation
      targetPopulation={targetPopulation}
      screenBeneficiary={businessAreaData?.businessArea?.screenBeneficiary}
    />
  );
};
