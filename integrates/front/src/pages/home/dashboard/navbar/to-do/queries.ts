import { gql } from "@apollo/client";

const GET_ME_VULNERABILITIES_ASSIGNED_IDS = gql`
  query GetMeVulnerabilitiesAssignedIds {
    me(callerOrigin: "FRONT") {
      vulnerabilitiesAssigned {
        id
      }
      userEmail
      __typename
    }
  }
`;

export { GET_ME_VULNERABILITIES_ASSIGNED_IDS };
