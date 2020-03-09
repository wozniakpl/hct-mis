import { gql } from 'apollo-boost';

export const AllTargetPopulations = gql`
  query AllTargetPopulations(
    $after: String
    $before: String
    $first: Int
    $last: Int
    $orderBy: String
  ) {
    allTargetPopulation(
      after: $after
      before: $before
      first: $first
      last: $last
      orderBy: $orderBy
    ) {
      edges {
        node {
          id
          name
          status
          createdAt
          lastEditedAt
          totalHouseholds
          totalFamilySize
          createdBy {
            firstName
            lastName
          }
        }
        cursor
      }
      totalCount
      edgeCount
    }
  }
`;
