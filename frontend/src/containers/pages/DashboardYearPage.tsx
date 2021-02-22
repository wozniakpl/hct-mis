import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Grid } from '@material-ui/core';
import { TabPanel } from '../../components/TabPanel';
import { DashboardPaper } from '../../components/Dashboard/DashboardPaper';
import { ProgrammesBySector } from '../../components/Dashboard/charts/ProgrammesBySector';
import { TotalTransferredByMonth } from '../../components/Dashboard/charts/TotalTransferredByMonth';
import { VolumeByDeliveryMechanism } from '../../components/Dashboard/charts/VolumeByDeliveryMechanism';
import { PaymentsChart } from '../../components/Dashboard/charts/PaymentsChart';
import { GrievancesSection } from '../../components/Dashboard/sections/GrievancesSection';
import { TotalNumberOfIndividualsReachedSection } from '../../components/Dashboard/sections/TotalNumberOfIndividualsReachedSection';
import { TotalNumberOfChildrenReachedSection } from '../../components/Dashboard/sections/TotalNumberOfChildrenReachedSection';
import { TotalNumberOfHouseholdsReachedSection } from '../../components/Dashboard/sections/TotalNumberOfHouseholdsReachedSection';
import { TotalAmountTransferredSection } from '../../components/Dashboard/sections/TotalAmountTransferredSection';
import { PaymentVerificationSection } from '../../components/Dashboard/sections/PaymentVerificationSection';
import { TotalAmountTransferredSectionByCountry } from '../../components/Dashboard/sections/TotalAmountTransferredByCountrySection';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import {
  useAllChartsQuery,
  useGlobalAreaChartsLazyQuery,
  useCountryChartsLazyQuery,
} from '../../__generated__/graphql';
import { LoadingComponent } from '../../components/LoadingComponent';
import { TotalAmountTransferredSectionByAdminAreaSection } from '../../components/Dashboard/sections/TotalAmountTransferredByAdminAreaSection';

const PaddingContainer = styled.div`
  padding: 20px;
`;
const PadddingLeftContainer = styled.div`
  padding-left: 20px;
`;
const CardTextLight = styled.div`
  text-transform: capitalize;
  color: #a4a4a4;
  font-weight: 500;
  font-size: ${(props) => (props.large ? '16px' : '12px')};
`;

interface DashboardYearPageProps {
  year: string;
  selectedTab: number;
  filter;
}
export function DashboardYearPage({
  year,
  selectedTab,
  filter,
}: DashboardYearPageProps): React.ReactElement {
  const businessArea = useBusinessArea();
  const isGlobal = businessArea === 'global';
  const [orderBy, setOrderBy] = useState('totalCashTransferred');
  const [order, setOrder] = useState('desc');

  const sharedVariables = {
    year: parseInt(year, 10),
  };
  const countryVariables = {
    program: filter.program,
    administrativeArea: filter.administrativeArea?.node?.id,
  };
  const { data, loading } = useAllChartsQuery({
    variables: {
      ...sharedVariables,
      businessAreaSlug: businessArea,
      ...(!isGlobal && countryVariables),
    },
  });
  const [
    loadGlobal,
    { data: globalData, loading: globalLoading },
  ] = useGlobalAreaChartsLazyQuery({
    variables: sharedVariables,
  });
  const [
    loadCountry,
    {
      data: countryData,
      loading: countryLoading,
      refetch: refetchAdminAreaChart,
    },
  ] = useCountryChartsLazyQuery({
    variables: {
      ...sharedVariables,
      businessAreaSlug: businessArea,
      ...countryVariables,
      orderBy,
      order,
    },
  });
  useEffect(() => {
    if (isGlobal) {
      loadGlobal();
    } else {
      loadCountry();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [businessArea]);

  const handleSortAdminArea = (event, property) => {
    let direction = '';
    if (property !== orderBy) {
      setOrderBy(property.toString());
      direction = order;
    } else {
      direction = order === 'desc' ? 'asc' : 'desc';
      setOrder(direction);
    }
    const variablesRefetch = {
      ...sharedVariables,
      businessAreaSlug: businessArea,
      ...countryVariables,
      orderBy: property,
      order: direction,
    };
    refetchAdminAreaChart(variablesRefetch);
  };

  if (isGlobal) {
    if (loading || globalLoading) return <LoadingComponent />;
    if (!data || !globalData) return null;
  } else {
    if (loading || countryLoading) return <LoadingComponent />;
    if (!data) return null;
  }
  return (
    <TabPanel value={selectedTab} index={selectedTab}>
      <PaddingContainer>
        <Grid container>
          <Grid item xs={8}>
            <TotalAmountTransferredSection
              data={data.sectionTotalTransferred}
            />
            <TotalAmountTransferredSectionByCountry
              data={globalData?.chartTotalTransferredCashByCountry}
            />
            <DashboardPaper title='Number of Programmes by Sector'>
              <ProgrammesBySector data={data.chartProgrammesBySector} />
            </DashboardPaper>
            <DashboardPaper title='Total Tranferred by Month'>
              <TotalTransferredByMonth
                data={data.chartTotalTransferredByMonth}
              />
            </DashboardPaper>
            <TotalAmountTransferredSectionByAdminAreaSection
              data={countryData?.tableTotalCashTransferredByAdministrativeArea}
              handleSort={handleSortAdminArea}
              order={order}
              orderBy={orderBy}
            />
            <PaymentVerificationSection data={data.chartPaymentVerification} />
          </Grid>
          <Grid item xs={4}>
            <PadddingLeftContainer>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <TotalNumberOfHouseholdsReachedSection
                    data={data.sectionHouseholdsReached}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TotalNumberOfIndividualsReachedSection
                    data={data.sectionIndividualsReached}
                    chartDataIndividuals={
                      data.chartIndividualsReachedByAgeAndGender
                    }
                    chartDataIndividualsDisability={
                      data.chartIndividualsWithDisabilityReachedByAge
                    }
                  />
                </Grid>
                <Grid item xs={12}>
                  <TotalNumberOfChildrenReachedSection
                    data={data.sectionChildReached}
                  />
                </Grid>
                <Grid item xs={12}>
                  <DashboardPaper title='Volume by Delivery Mechanism in USD'>
                    <CardTextLight large>
                      Delivery type in CashAssist
                    </CardTextLight>
                    <VolumeByDeliveryMechanism
                      data={data.chartVolumeByDeliveryMechanism}
                    />
                  </DashboardPaper>
                  <GrievancesSection data={data.chartGrievances} />
                  <DashboardPaper title='Payments'>
                    <PaymentsChart data={data.chartPayment} />
                  </DashboardPaper>
                </Grid>
              </Grid>
            </PadddingLeftContainer>
          </Grid>
        </Grid>
      </PaddingContainer>
    </TabPanel>
  );
}
