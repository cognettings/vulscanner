import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENT_DESCRIPTION: DocumentNode = gql`
  query GetEventDescription(
    $canRetrieveHacker: Boolean!
    $eventId: String!
    $groupName: String!
  ) {
    event(groupName: $groupName, identifier: $eventId) {
      affectedReattacks {
        findingId
        id
        where
        specific
      }
      client
      closingDate
      detail
      eventType
      eventStatus
      hacker @include(if: $canRetrieveHacker)
      id
      otherSolvingReason
      solvingReason
    }
  }
`;

const REJECT_EVENT_SOLUTION_MUTATION: DocumentNode = gql`
  mutation RejectEventSolutionMutation(
    $comments: String!
    $eventId: String!
    $groupName: String!
  ) {
    rejectEventSolution(
      comments: $comments
      eventId: $eventId
      groupName: $groupName
    ) {
      success
    }
  }
`;

const SOLVE_EVENT_MUTATION: DocumentNode = gql`
  mutation SolveEventMutation(
    $eventId: String!
    $groupName: String!
    $other: String
    $reason: SolveEventReason!
  ) {
    solveEvent(
      eventId: $eventId
      groupName: $groupName
      reason: $reason
      other: $other
    ) {
      success
    }
  }
`;

const UPDATE_EVENT_MUTATION: DocumentNode = gql`
  mutation UpdateEventMutation(
    $eventId: String!
    $eventType: EventType
    $groupName: String!
    $otherSolvingReason: String
    $solvingReason: SolveEventReason
  ) {
    updateEvent(
      eventId: $eventId
      eventType: $eventType
      groupName: $groupName
      otherSolvingReason: $otherSolvingReason
      solvingReason: $solvingReason
    ) {
      success
    }
  }
`;

export {
  GET_EVENT_DESCRIPTION,
  REJECT_EVENT_SOLUTION_MUTATION,
  SOLVE_EVENT_MUTATION,
  UPDATE_EVENT_MUTATION,
};
