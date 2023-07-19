import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_DESCRIPTION: DocumentNode = gql`
  query GetFindingDescription(
    $canRetrieveHacker: Boolean!
    $canRetrieveSorts: Boolean!
    $findingId: String!
  ) {
    finding(identifier: $findingId) {
      attackVectorDescription
      description
      hacker @include(if: $canRetrieveHacker)
      id
      openVulnerabilities
      recommendation
      releaseDate
      sorts @include(if: $canRetrieveSorts)
      status
      threat
      title
      unfulfilledRequirements {
        id
        summary
      }
    }
  }
`;

const GET_LANGUAGE: DocumentNode = gql`
  query GetLanguageQuery($groupName: String!) {
    group(groupName: $groupName) {
      name
      language
    }
  }
`;

const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateFindingDescription(
    $attackVectorDescription: String!
    $description: String!
    $findingId: String!
    $recommendation: String!
    $sorts: Sorts!
    $threat: String!
    $title: String!
    $unfulfilledRequirements: [String!]
  ) {
    updateDescription(
      attackVectorDescription: $attackVectorDescription
      description: $description
      findingId: $findingId
      recommendation: $recommendation
      sorts: $sorts
      threat: $threat
      title: $title
      unfulfilledRequirements: $unfulfilledRequirements
    ) {
      success
    }
  }
`;

export { GET_FINDING_DESCRIPTION, GET_LANGUAGE, UPDATE_DESCRIPTION_MUTATION };
