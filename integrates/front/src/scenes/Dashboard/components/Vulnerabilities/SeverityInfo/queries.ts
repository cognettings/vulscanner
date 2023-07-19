import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULN_SEVERITY_INFO: DocumentNode = gql`
  query GetVulnSeverityInfo($vulnId: String!) {
    vulnerability(uuid: $vulnId) {
      id
      severityTemporalScore
      severityVector
    }
  }
`;

const UPDATE_VULNERABILITIES_SEVERITY: DocumentNode = gql`
  mutation UpdateVulnerabilitiesSeverity(
    $cvssVector: String!
    $findingId: ID!
    $vulnerabilityIds: [ID!]!
  ) {
    updateVulnerabilitiesSeverity(
      cvssVector: $cvssVector
      findingId: $findingId
      vulnerabilityIds: $vulnerabilityIds
    ) {
      success
    }
  }
`;

export { GET_VULN_SEVERITY_INFO, UPDATE_VULNERABILITIES_SEVERITY };
