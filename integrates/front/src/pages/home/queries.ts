import { gql } from "@apollo/client";

interface ICurrentUser {
  me: {
    enrolled: boolean;
    permissions: string[];
    phone: {
      callingCountryCode: string;
      nationalNumber: string;
    } | null;
    tours: {
      newGroup: boolean;
      newRiskExposure: boolean;
      newRoot: boolean;
      welcome: boolean;
    };
    trial: {
      completed: boolean;
    } | null;
    userEmail: string;
    userName: string;
  };
}

// Keep this query light weight for a smooth post-login experience
const GET_CURRENT_USER = gql`
  query GetCurrentUser {
    me {
      enrolled
      permissions
      phone {
        callingCountryCode
        nationalNumber
      }
      tours {
        newGroup
        newRiskExposure
        newRoot
        welcome
      }
      trial {
        completed
      }
      userEmail
      userName
    }
  }
`;

const GET_ROOTS = gql`
  query GetRoots($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          id
          nickname
        }
        ... on IPRoot {
          id
          nickname
        }
        ... on URLRoot {
          id
          nickname
        }
      }
    }
  }
`;

export type { ICurrentUser };
export { GET_CURRENT_USER, GET_ROOTS };
