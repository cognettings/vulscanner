import { gql } from "@apollo/client";

const GET_GROUP_SERVICES = gql`
  query GetGroupServices($groupName: String!) {
    group(groupName: $groupName) {
      name
      serviceAttributes
    }
  }
`;

const GET_STAKEHOLDER_TRIAL = gql`
  query GetStakeholderTrial {
    me {
      userEmail
      trial {
        extensionDate
        extensionDays
        completed
        startDate
        state
      }
    }
  }
`;

const UPDATE_TOURS = gql`
  mutation updateTours(
    $newGroup: Boolean!
    $newRiskExposure: Boolean!
    $newRoot: Boolean!
    $welcome: Boolean!
  ) {
    updateTours(
      tours: {
        newGroup: $newGroup
        newRiskExposure: $newRiskExposure
        newRoot: $newRoot
        welcome: $welcome
      }
    ) {
      success
    }
  }
`;

export { GET_GROUP_SERVICES, GET_STAKEHOLDER_TRIAL, UPDATE_TOURS };
