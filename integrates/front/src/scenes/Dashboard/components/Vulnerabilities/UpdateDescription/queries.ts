import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_VULNERABILITY_MUTATION: DocumentNode = gql`
  mutation UpdateVulnerabilityMutation(
    $findingId: String!
    $severity: Int
    $tag: String
    $assigned: String
    $vulnerabilityId: ID!
    $externalBugTrackingSystem: String
    $acceptanceDate: String
    $justification: String!
    $source: VulnerabilitySource
    $treatment: UpdateClientDescriptionTreatment!
    $isVulnDescriptionChanged: Boolean!
    $isVulnTreatmentChanged: Boolean!
    $isVulnTreatmentDescriptionChanged: Boolean!
  ) {
    updateVulnerabilityDescription(
      source: $source
      vulnerabilityId: $vulnerabilityId
    ) @include(if: $isVulnDescriptionChanged) {
      success
    }
    updateVulnerabilityTreatment(
      externalBugTrackingSystem: $externalBugTrackingSystem
      findingId: $findingId
      severity: $severity
      tag: $tag
      vulnerabilityId: $vulnerabilityId
    ) @include(if: $isVulnTreatmentDescriptionChanged) {
      success
    }
    updateVulnerabilitiesTreatment(
      acceptanceDate: $acceptanceDate
      findingId: $findingId
      justification: $justification
      treatment: $treatment
      assigned: $assigned
      vulnerabilityId: $vulnerabilityId
    ) @include(if: $isVulnTreatmentChanged) {
      success
    }
  }
`;

const SEND_ASSIGNED_NOTIFICATION: DocumentNode = gql`
  mutation SendAssignedNotification(
    $findingId: String!
    $vulnerabilities: [String]!
  ) {
    sendAssignedNotification(
      findingId: $findingId
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const REMOVE_TAGS_MUTATION: DocumentNode = gql`
  mutation RemoveTagsVuln(
    $findingId: String!
    $tag: String
    $vulnerabilities: [String]!
  ) {
    removeTags(
      findingId: $findingId
      tag: $tag
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const REQUEST_VULNS_ZERO_RISK: DocumentNode = gql`
  mutation RequestVulnerabilitiesZeroRisk(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    requestVulnerabilitiesZeroRisk(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export {
  REMOVE_TAGS_MUTATION,
  REQUEST_VULNS_ZERO_RISK,
  UPDATE_VULNERABILITY_MUTATION,
  SEND_ASSIGNED_NOTIFICATION,
};
