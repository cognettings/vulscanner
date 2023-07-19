import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENT_CONSULTING: DocumentNode = gql`
  query GetEventConsulting($eventId: String!, $groupName: String!) {
    event(groupName: $groupName, identifier: $eventId) {
      consulting {
        id
        content
        created
        email
        fullName
        modified
        parentComment
      }
      id
    }
  }
`;

const ADD_EVENT_CONSULT: DocumentNode = gql`
  mutation AddEventConsult(
    $content: String!
    $eventId: String!
    $groupName: String!
    $parentComment: GenericScalar!
  ) {
    addEventConsult(
      content: $content
      eventId: $eventId
      groupName: $groupName
      parentComment: $parentComment
    ) {
      commentId
      success
    }
  }
`;

export { GET_EVENT_CONSULTING, ADD_EVENT_CONSULT };
