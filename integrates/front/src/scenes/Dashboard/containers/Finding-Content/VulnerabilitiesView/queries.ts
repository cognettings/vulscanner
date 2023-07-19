import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnFields on Vulnerability {
    advisories {
      cve
      package
      vulnerableVersion
    }
    externalBugTrackingSystem
    findingId
    id
    lastStateDate
    lastTreatmentDate
    lastVerificationDate
    remediated
    reportDate
    rootNickname
    severity
    severityTemporalScore
    source
    specific
    state
    stream
    tag
    technique
    treatmentAcceptanceDate
    treatmentAcceptanceStatus
    treatmentAssigned
    treatmentJustification
    treatmentStatus
    treatmentUser
    verification
    vulnerabilityType
    where
    zeroRisk
  }
`;

const GET_FINDING_INFO: DocumentNode = gql`
  query GetFindingInfo($findingId: String!) {
    finding(identifier: $findingId) {
      id
      remediated
      releaseDate
      status
      totalOpenCVSSF
      verified
    }
  }
`;

const GET_FINDING_NZR_VULNS: DocumentNode = gql`
  query GetFindingNzrVulns(
    $after: String
    $findingId: String!
    $first: Int
    $state: VulnerabilityState
  ) {
    finding(identifier: $findingId) {
      __typename
      id
      vulnerabilitiesConnection(after: $after, first: $first, state: $state) {
        edges {
          node {
            ...vulnFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

const GET_FINDING_VULN_DRAFTS: DocumentNode = gql`
  query GetFindingVulnDrafts(
    $after: String
    $canRetrieveDrafts: Boolean!
    $findingId: String!
    $first: Int
  ) {
    finding(identifier: $findingId) {
      __typename
      id
      draftsConnection(after: $after, first: $first)
        @include(if: $canRetrieveDrafts) {
        edges {
          node {
            ...vulnFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

const GET_FINDING_ZR_VULNS: DocumentNode = gql`
  query GetFindingZrVulns(
    $after: String
    $canRetrieveZeroRisk: Boolean!
    $findingId: String!
    $first: Int
  ) {
    finding(identifier: $findingId) {
      __typename
      id
      zeroRiskConnection(after: $after, first: $first)
        @include(if: $canRetrieveZeroRisk) {
        edges {
          node {
            ...vulnFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

const RESUBMIT_VULNERABILITIES: DocumentNode = gql`
  mutation ResubmitVulnerabilitiesRequest(
    $findingId: String!
    $vulnerabilities: [String!]!
  ) {
    resubmitVulnerabilities(
      findingId: $findingId
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const CLOSE_VULNERABILITIES: DocumentNode = gql`
  mutation CloseVulnerabilities(
    $findingId: String!
    $vulnerabilities: [String!]!
  ) {
    closeVulnerabilities(
      findingId: $findingId
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const SEND_VULNERABILITY_NOTIFICATION: DocumentNode = gql`
  mutation SendVulnerabilityNotification($findingId: String!) {
    sendVulnerabilityNotification(findingId: $findingId) {
      success
    }
  }
`;

export {
  VULNS_FRAGMENT,
  GET_FINDING_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_VULN_DRAFTS,
  GET_FINDING_ZR_VULNS,
  CLOSE_VULNERABILITIES,
  RESUBMIT_VULNERABILITIES,
  SEND_VULNERABILITY_NOTIFICATION,
};
