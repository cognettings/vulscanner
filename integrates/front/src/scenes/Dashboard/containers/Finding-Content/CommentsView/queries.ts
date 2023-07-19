import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const FRAGMENTS: Record<string, DocumentNode> = {
  commentFields: gql`
    fragment commentFields on Consult {
      id
      content
      created
      email
      fullName
      modified
      parentComment
    }
  `,
  consultFields: gql`
    fragment consultFields on Consult {
      id
      content
      created
      email
      fullName
      modified
      parentComment
    }
  `,
};

const GET_FINDING_CONSULTING: DocumentNode = gql`
  query GetFindingConsulting($findingId: String!) {
    finding(identifier: $findingId) {
      consulting {
        ...consultFields
      }
      id
    }
  }
  ${FRAGMENTS.consultFields}
`;

const GET_FINDING_OBSERVATIONS: DocumentNode = gql`
  query GetFindingObservations($findingId: String!) {
    finding(identifier: $findingId) {
      observations {
        ...commentFields
      }
      id
    }
  }
  ${FRAGMENTS.commentFields}
`;

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

export {
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
  ADD_FINDING_CONSULT,
};
