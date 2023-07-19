import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_HEADER: DocumentNode = gql`
  query GetFindingHeader(
    $findingId: String!
    $canRetrieveHacker: Boolean! = false
  ) {
    finding(identifier: $findingId) {
      closedVulns: closedVulnerabilities
      currentState
      hacker @include(if: $canRetrieveHacker)
      id
      maxOpenSeverityScore
      minTimeToRemediate
      openVulns: openVulnerabilities
      releaseDate
      status
      title
      totalOpenCVSSF
    }
  }
`;

const REMOVE_FINDING_MUTATION: DocumentNode = gql`
  mutation RemoveFindingMutation(
    $findingId: String!
    $justification: RemoveFindingJustification!
  ) {
    removeFinding(findingId: $findingId, justification: $justification) {
      success
    }
  }
`;

export { GET_FINDING_HEADER, REMOVE_FINDING_MUTATION };
