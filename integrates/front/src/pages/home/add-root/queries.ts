import { gql } from "@apollo/client";

const GET_CURRENT_USER = gql`
  query GetCurrentUser {
    me {
      organizations {
        groups {
          name
        }
        id
        name
      }
      userEmail
      userName
    }
  }
`;

export { GET_CURRENT_USER };
