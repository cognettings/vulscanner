import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FORCES_TOKEN: DocumentNode = gql`
  query GetForcesToken($groupName: String!) {
    group(groupName: $groupName) {
      forcesExpDate
      forcesToken
      name
    }
  }
`;

const UPDATE_FORCES_TOKEN_MUTATION: DocumentNode = gql`
  mutation UpdateForcesAccessTokenMutation($groupName: String!) {
    updateForcesAccessToken(groupName: $groupName) {
      success
      sessionJwt
    }
  }
`;

export { GET_FORCES_TOKEN, UPDATE_FORCES_TOKEN_MUTATION };
