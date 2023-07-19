import { gql } from "@apollo/client";

const GET_FINDING_EVIDENCE_DRAFTS = gql`
  query GetFindingEvidenceDrafts($after: String, $first: Int) {
    me {
      userEmail
      findingEvidenceDrafts(after: $after, first: $first) {
        edges {
          node {
            groupName
            id
            title
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        total
      }
      __typename
    }
  }
`;

export { GET_FINDING_EVIDENCE_DRAFTS };
