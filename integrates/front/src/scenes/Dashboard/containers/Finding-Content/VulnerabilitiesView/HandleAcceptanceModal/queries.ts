import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_FINDING_CONSULT: DocumentNode = gql`
  mutation AddFindingConsult(
    $content: String!
    $findingId: String!
    $parentComment: GenericScalar!
    $type: FindingConsultType!
  ) {
    addFindingConsult(
      content: $content
      findingId: $findingId
      parentComment: $parentComment
      type: $type
    ) {
      commentId
      success
    }
  }
`;

const HANDLE_VULNS_ACCEPTANCE: DocumentNode = gql`
  mutation HandleVulnerabilitiesAcceptance(
    $acceptedVulnerabilities: [String]!
    $findingId: String!
    $justification: String!
    $rejectedVulnerabilities: [String]!
  ) {
    handleVulnerabilitiesAcceptance(
      findingId: $findingId
      justification: $justification
      acceptedVulnerabilities: $acceptedVulnerabilities
      rejectedVulnerabilities: $rejectedVulnerabilities
    ) {
      success
    }
  }
`;

const CONFIRM_VULNERABILITIES: DocumentNode = gql`
  mutation ConfirmVulnerabilities(
    $findingId: String!
    $vulnerabilities: [String!]!
  ) {
    confirmVulnerabilities(
      findingId: $findingId
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const CONFIRM_VULNERABILITIES_ZERO_RISK: DocumentNode = gql`
  mutation ConfirmVulnerabilitiesZeroRisk(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    confirmVulnerabilitiesZeroRisk(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const REJECT_VULNERABILITIES: DocumentNode = gql`
  mutation RejectVulnerabilities(
    $findingId: String!
    $reasons: [VulnerabilityRejectionReason!]!
    $otherReason: String
    $vulnerabilities: [String!]!
  ) {
    rejectVulnerabilities(
      findingId: $findingId
      reasons: $reasons
      otherReason: $otherReason
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

const REJECT_VULNERABILITIES_ZERO_RISK: DocumentNode = gql`
  mutation RejectVulnerabilitiesZeroRisk(
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    rejectVulnerabilitiesZeroRisk(
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export {
  ADD_FINDING_CONSULT,
  CONFIRM_VULNERABILITIES,
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTANCE,
  REJECT_VULNERABILITIES,
  REJECT_VULNERABILITIES_ZERO_RISK,
};
