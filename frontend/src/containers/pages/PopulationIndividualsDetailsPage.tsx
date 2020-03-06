import React from 'react';
import styled from 'styled-components';
import { useParams } from 'react-router-dom';
import { PageHeader } from '../../components/PageHeader';
import { BreadCrumbsItem } from '../../components/BreadCrumbs';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { IndividualsBioData } from '../../components/population/IndividualBioData';
import {
  IndividualNode,
  useIndividualQuery,
} from '../../__generated__/graphql';
import { IndividualContactDetails } from '../../components/population/IndividualContactDetails';
import { IndividualVulnerabilities } from '../../components/population/IndividualVunerabilities';
import { UniversalActivityLogTable } from '../tables/UniversalActivityLogTable';
import { decodeIdString } from '../../utils/utils';

const Container = styled.div`
  padding: 20px;
  && {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
`;

export function PopulationIndividualsDetailsPage(): React.ReactElement {
  const { id } = useParams();
  const businessArea = useBusinessArea();
  const { data, loading } = useIndividualQuery({
    variables: {
      id,
    },
  });

  if (loading) return null;

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: 'Individuals',
      to: `/${businessArea}/population/individuals`,
    },
  ];

  const { individual } = data;
  return (
    <div>
      <PageHeader
        title={`Individual ID: ${decodeIdString(id)}`}
        breadCrumbs={breadCrumbsItems}
      />
      <Container>
        <IndividualsBioData individual={individual as IndividualNode} />
        <IndividualContactDetails individual={individual as IndividualNode} />
        <IndividualVulnerabilities individual={individual as IndividualNode} />
        <UniversalActivityLogTable objectId={individual.id} />
      </Container>
    </div>
  );
}
