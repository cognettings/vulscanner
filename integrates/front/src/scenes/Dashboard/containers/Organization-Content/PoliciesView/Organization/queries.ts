import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_POLICIES: DocumentNode = gql`
  query GetOrganizationPolicies($organizationId: String!) {
    organization(organizationId: $organizationId) {
      findingPolicies {
        id
        lastStatusUpdate
        name
        status
        tags
      }
      inactivityPeriod
      maxAcceptanceDays
      maxAcceptanceSeverity
      maxNumberAcceptances
      minAcceptanceSeverity
      minBreakingSeverity
      vulnerabilityGracePeriod
      name
    }
  }
`;

const UPDATE_ORGANIZATION_POLICIES: DocumentNode = gql`
  mutation UpdateOrganizationPolicies(
    $inactivityPeriod: Int
    $maxAcceptanceDays: Int
    $maxAcceptanceSeverity: Float
    $maxNumberAcceptances: Int
    $minAcceptanceSeverity: Float
    $minBreakingSeverity: Float
    $vulnerabilityGracePeriod: Int
    $organizationId: String!
    $organizationName: String!
  ) {
    updateOrganizationPolicies(
      inactivityPeriod: $inactivityPeriod
      maxAcceptanceDays: $maxAcceptanceDays
      maxAcceptanceSeverity: $maxAcceptanceSeverity
      maxNumberAcceptances: $maxNumberAcceptances
      minAcceptanceSeverity: $minAcceptanceSeverity
      minBreakingSeverity: $minBreakingSeverity
      vulnerabilityGracePeriod: $vulnerabilityGracePeriod
      organizationId: $organizationId
      organizationName: $organizationName
    ) {
      success
    }
  }
`;

export { GET_ORGANIZATION_POLICIES, UPDATE_ORGANIZATION_POLICIES };
