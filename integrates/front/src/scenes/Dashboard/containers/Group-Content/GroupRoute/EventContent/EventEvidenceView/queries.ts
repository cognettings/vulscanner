import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const DOWNLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation DownloadEventFileMutation(
    $eventId: String!
    $fileName: String!
    $groupName: String!
  ) {
    downloadEventFile(
      eventId: $eventId
      fileName: $fileName
      groupName: $groupName
    ) {
      success
      url
    }
  }
`;

const GET_EVENT_EVIDENCES: DocumentNode = gql`
  query GetEventEvidences($eventId: String!, $groupName: String!) {
    event(groupName: $groupName, identifier: $eventId) {
      eventStatus
      evidences {
        file1 {
          fileName
          date
        }
        image1 {
          fileName
          date
        }
        image2 {
          fileName
          date
        }
        image3 {
          fileName
          date
        }
        image4 {
          fileName
          date
        }
        image5 {
          fileName
          date
        }
        image6 {
          fileName
          date
        }
      }
      id
    }
  }
`;

const UPDATE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation UpdateEventEvidenceMutation(
    $eventId: String!
    $evidenceType: EventEvidenceType!
    $groupName: String!
    $file: Upload!
  ) {
    updateEventEvidence(
      eventId: $eventId
      evidenceType: $evidenceType
      groupName: $groupName
      file: $file
    ) {
      success
    }
  }
`;

const REMOVE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation RemoveEventEvidenceMutation(
    $eventId: String!
    $evidenceType: EventEvidenceType!
    $groupName: String!
  ) {
    removeEventEvidence(
      eventId: $eventId
      evidenceType: $evidenceType
      groupName: $groupName
    ) {
      success
    }
  }
`;

export {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
  UPDATE_EVIDENCE_MUTATION,
  REMOVE_EVIDENCE_MUTATION,
};
