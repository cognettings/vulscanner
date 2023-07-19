import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_EVENT_HEADER: DocumentNode = gql`
  query GetEventHeader($eventId: String!, $groupName: String!) {
    event(groupName: $groupName, identifier: $eventId) {
      eventDate
      eventStatus
      eventType
      id
    }
  }
`;
