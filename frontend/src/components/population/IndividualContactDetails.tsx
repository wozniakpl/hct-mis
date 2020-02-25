import React from 'react';
import styled from 'styled-components';
import { Paper, Typography, Grid } from '@material-ui/core';
import { LabelizedField } from '../LabelizedField';
import { IndividualNode } from '../../__generated__/graphql';

const Overview = styled(Paper)`
  padding: ${({ theme }) => theme.spacing(8)}px
    ${({ theme }) => theme.spacing(11)}px;
  margin-top: ${({ theme }) => theme.spacing(6)}px;
`;

const Title = styled.div`
  width: 100%;
  padding-bottom: ${({ theme }) => theme.spacing(8)}px;
`;

interface IndividualContactProps {
  individual: IndividualNode;
}
export function IndividualContactDetails({
  individual,
}: IndividualContactProps): React.ReactElement {
  const { phoneNumber, household } = individual;

  return (
    <Overview>
      <Title>
        <Typography variant='h6'>Contact Details</Typography>
      </Title>
      <Grid container spacing={6}>
        <Grid item xs={4}>
          <LabelizedField label='Phone Number'>
            <div>{phoneNumber}</div>
          </LabelizedField>
        </Grid>
        <Grid item xs={8}>
          <LabelizedField label='Alternate Phone Number'>
            <div>-</div>
          </LabelizedField>
        </Grid>
        <Grid item xs={4}>
          <LabelizedField label='Address'>
            <div>{household.address ? household.address : '-'}</div>
          </LabelizedField>
        </Grid>
        <Grid item xs={4}>
          <LabelizedField label='Location Level'>
            <div>{household.location ? household.location.level : '-'}</div>
          </LabelizedField>
        </Grid>
        <Grid item xs={4}>
          <LabelizedField label='Location Name'>
            <div>{household.location ? household.location.title : '-'}</div>
          </LabelizedField>
        </Grid>
      </Grid>
    </Overview>
  );
}
