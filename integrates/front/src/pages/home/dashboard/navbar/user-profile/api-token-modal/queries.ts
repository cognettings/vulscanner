import { gql } from "@apollo/client";

const GET_ACCESS_TOKEN = gql`
  query GetAccessTokenQuery {
    me(callerOrigin: "FRONT") {
      accessTokens {
        __typename
        name
        id
        issuedAt
        lastUse
      }
      userEmail
    }
  }
`;

const INVALIDATE_ACCESS_TOKEN_MUTATION = gql`
  mutation InvalidateAccessTokenMutation($id: ID) {
    invalidateAccessToken(id: $id) {
      success
    }
  }
`;

const ADD_ACCESS_TOKEN = gql`
  mutation AddAccessToken($expirationTime: Int!, $name: String!) {
    addAccessToken(expirationTime: $expirationTime, name: $name) {
      sessionJwt
      success
    }
  }
`;

export { ADD_ACCESS_TOKEN, GET_ACCESS_TOKEN, INVALIDATE_ACCESS_TOKEN_MUTATION };
