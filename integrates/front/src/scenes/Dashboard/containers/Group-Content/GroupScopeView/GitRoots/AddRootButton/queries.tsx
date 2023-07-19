import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_CREDENTIALS: DocumentNode = gql`
  query GetOrganizationCredentials($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      name
      credentials {
        __typename
        azureOrganization
        id
        isPat
        isToken
        name
        oauthType
        owner
        type
      }
    }
  }
`;

export { GET_ORGANIZATION_CREDENTIALS };
