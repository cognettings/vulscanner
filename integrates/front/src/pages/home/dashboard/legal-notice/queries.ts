import { gql } from "@apollo/client";

interface IUserRemember {
  me: {
    __typename: "Me";
    remember: boolean;
    userEmail: string;
  };
}

const GET_USER_REMEMBER = gql`
  query GetUserRemember {
    me {
      remember
      userEmail
    }
  }
`;

interface IAcceptLegal {
  acceptLegal: {
    success: boolean;
  };
}

const ACCEPT_LEGAL_MUTATION = gql`
  mutation AcceptLegalMutation($remember: Boolean!) {
    acceptLegal(remember: $remember) {
      success
    }
  }
`;

export { ACCEPT_LEGAL_MUTATION, GET_USER_REMEMBER };
export type { IAcceptLegal, IUserRemember };
