import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnGroupFields on Vulnerability {
    state
    externalBugTrackingSystem
    findingId
    id
    lastTreatmentDate
    lastVerificationDate
    remediated
    reportDate
    rootNickname
    severity
    severityTemporalScore
    specific
    source
    stream
    tag
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

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetGroupVulnerabilities(
    $after: String
    $first: Int
    $groupName: String!
    $root: String
    $search: String
    $treatment: String
    $type: String
    $stateStatus: String
    $verificationStatus: String
    $zeroRisk: VulnerabilityZeroRiskStatus
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilities(
        after: $after
        first: $first
        root: $root
        search: $search
        treatment: $treatment
        type: $type
        stateStatus: $stateStatus
        verificationStatus: $verificationStatus
        zeroRisk: $zeroRisk
      ) {
        edges {
          node {
            groupName
            finding {
              id
              title
            }
            ...vulnGroupFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        total
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

const GET_GROUP_VULNERABILITY_DRAFTS: DocumentNode = gql`
  query GetGroupVulnerabilityDrafts(
    $after: String
    $canRetrieveDrafts: Boolean!
    $first: Int
    $groupName: String!
    $root: String
    $search: String
    $type: String
    $stateStatus: String
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilityDrafts(
        after: $after
        first: $first
        root: $root
        search: $search
        type: $type
        stateStatus: $stateStatus
      ) @include(if: $canRetrieveDrafts) {
        edges {
          node {
            groupName
            finding {
              id
              title
            }
            ...vulnGroupFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        total
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

export { GET_GROUP_VULNERABILITIES, GET_GROUP_VULNERABILITY_DRAFTS };
