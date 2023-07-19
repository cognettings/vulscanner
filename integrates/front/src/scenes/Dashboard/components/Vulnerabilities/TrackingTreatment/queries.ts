import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULN_TREATMENT: DocumentNode = gql`
  query GetVulnTreatment($after: String, $vulnId: String!) {
    vulnerability(uuid: $vulnId) {
      id
      historicTreatmentConnection(after: $after) {
        edges {
          node {
            acceptanceDate
            acceptanceStatus
            assigned
            date
            justification
            user
            treatment
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
`;

export { GET_VULN_TREATMENT };
