import { gql } from 'apollo-boost';

export const BulkUpdateGrievanceUrgency = gql`
  mutation BulkUpdateGrievanceUrgency(
    $grievanceTicketIds: [ID]!
    $urgency: Int!
    $businessAreaSlug: String!
  ) {
    bulkUpdateGrievanceUrgency(
      grievanceTicketIds: $grievanceTicketIds
      urgency: $urgency
      businessAreaSlug: $businessAreaSlug
    ) {
      grievanceTickets {
        id
        urgency
      }
    }
  }
`;
