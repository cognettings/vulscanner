import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_UNFULFILLED_STANDARDS: DocumentNode = gql`
  query GetGroupUnfulfilledStandards($groupName: String!) {
    group(groupName: $groupName) {
      name
      compliance {
        unfulfilledStandards {
          standardId
          title
          unfulfilledRequirements {
            id
            title
          }
        }
      }
    }
  }
`;

const GET_UNFULFILLED_STANDARD_REPORT_URL: DocumentNode = gql`
  query RequestGroupReport(
    $groupName: String!
    $verificationCode: String!
    $unfulfilledStandards: [String!]
  ) {
    unfulfilledStandardReportUrl(
      groupName: $groupName
      verificationCode: $verificationCode
      unfulfilledStandards: $unfulfilledStandards
    )
  }
`;

export { GET_GROUP_UNFULFILLED_STANDARDS, GET_UNFULFILLED_STANDARD_REPORT_URL };
