import { Box, Typography } from '@material-ui/core';
import React, { useState } from 'react';
import styled from 'styled-components';
import { householdDetailed } from '../../apollo/fragments/HouseholdFragments';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { GRIEVANCE_TICKET_STATES } from '../../utils/constants';
import { decodeIdString } from '../../utils/utils';
import {
  GrievanceTicketQuery,
  useAllGrievanceTicketQuery,
  useExistingGrievanceTicketsQuery,
} from '../../__generated__/graphql';
import { ContentLink } from '../ContentLink';
import { LabelizedField } from '../LabelizedField';
import { LoadingComponent } from '../LoadingComponent';

const StyledBox = styled.div`
  border-color: #b1b1b5;
  border-bottom-width: 1px;
  border-bottom-style: solid;
  border-radius: 3px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 26px 22px;
`;
const Title = styled.div`
  padding-bottom: ${({ theme }) => theme.spacing(8)}px;
`;

const BlueBold = styled.div`
  color: ${({ theme }) => theme.hctPalette.navyBlue};
  font-weight: 500;
  cursor: pointer;
`;

export const OtherRelatedTickets = ({
  linkedTickets,
  ticket,
}: {
  linkedTickets: GrievanceTicketQuery['grievanceTicket']['linkedTickets']['edges'];
  ticket: GrievanceTicketQuery['grievanceTicket'];
}) => {
  const businessArea = useBusinessArea();
  const [show, setShow] = useState(false);

  const { data, loading } = useExistingGrievanceTicketsQuery({
    variables: {
      businessArea,
      category: ticket.category.toString(),
      household: ticket.household?.id || '',
    },
  });
  if (loading) return <LoadingComponent />;
  if (!data) return null;

  const householdTickets = data.existingGrievanceTickets.edges;
  console.log('😎: householdTickets', householdTickets);

  const renderIds = (tickets) =>
    tickets.length
      ? tickets.map((edge) => (
          <Box key={edge.node.id} mb={1}>
            <ContentLink
              href={`/${businessArea}/grievance-and-feedback/${edge.node.id}`}
            >
              {decodeIdString(edge.node.id)}
            </ContentLink>
          </Box>
        ))
      : '-';

  const openHouseholdTickets = householdTickets.length
    ? householdTickets.filter(
        (edge) => edge.node.status !== GRIEVANCE_TICKET_STATES.CLOSED,
      )
    : [];
  const closedHouseholdTickets = householdTickets.length
    ? householdTickets.filter(
        (edge) => edge.node.status === GRIEVANCE_TICKET_STATES.CLOSED,
      )
    : [];

  const openTickets = linkedTickets.length
    ? linkedTickets.filter(
        (edge) => edge.node.status !== GRIEVANCE_TICKET_STATES.CLOSED,
      )
    : [];
  const closedTickets = linkedTickets.length
    ? linkedTickets.filter(
        (edge) => edge.node.status === GRIEVANCE_TICKET_STATES.CLOSED,
      )
    : [];

  return linkedTickets.length || householdTickets.length ? (
    <StyledBox>
      <Title>
        <Typography variant='h6'>Other Related Tickets</Typography>
      </Title>
      <Box display='flex' flexDirection='column'>
        <LabelizedField label='For Household'>
          <>{renderIds(openHouseholdTickets)}</>
        </LabelizedField>
        <LabelizedField label='Tickets'>
          <>{renderIds(openTickets)}</>
        </LabelizedField>
        {!show && (closedTickets.length || closedHouseholdTickets.length) ? (
          <Box mt={3}>
            <BlueBold onClick={() => setShow(true)}>
              SHOW CLOSED TICKETS (
              {closedTickets.length + closedHouseholdTickets.length})
            </BlueBold>
          </Box>
        ) : null}
        {show && (
          <Box mb={3} mt={3}>
            <Typography>Closed Tickets</Typography>
            <LabelizedField label='For Household'>
              <>{renderIds(closedHouseholdTickets)}</>
            </LabelizedField>
            <LabelizedField label='Tickets'>
              <>{renderIds(closedTickets)}</>
            </LabelizedField>
          </Box>
        )}
        {show && (closedTickets.length || closedHouseholdTickets.length) ? (
          <BlueBold onClick={() => setShow(false)}>
            HIDE CLOSED TICKETS (
            {closedTickets.length + closedHouseholdTickets.length})
          </BlueBold>
        ) : null}
      </Box>
    </StyledBox>
  ) : null;
};
