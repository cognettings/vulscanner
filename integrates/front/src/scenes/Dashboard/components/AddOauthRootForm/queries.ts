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

const GET_INTEGRATION_REPOSITORIES: DocumentNode = gql`
  query GetOrganizationCredentials($credId: String!, $organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      name
      credential(id: $credId) {
        integrationRepositories {
          __typename
          branches
          name
          url
        }
      }
    }
  }
`;

const ADD_GIT_ROOT: DocumentNode = gql`
  mutation AddGitRoot(
    $branch: String!
    $credentials: RootCredentialsInput
    $environment: String!
    $gitignore: [String!]!
    $groupName: String!
    $includesHealthCheck: Boolean!
    $nickname: String!
    $url: String!
    $useVpn: Boolean!
  ) {
    addGitRoot(
      branch: $branch
      credentials: $credentials
      environment: $environment
      gitignore: $gitignore
      groupName: $groupName
      includesHealthCheck: $includesHealthCheck
      nickname: $nickname
      url: $url
      useVpn: $useVpn
    ) {
      success
    }
  }
`;

export {
  ADD_GIT_ROOT,
  GET_INTEGRATION_REPOSITORIES,
  GET_ORGANIZATION_CREDENTIALS,
};
