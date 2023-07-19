import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          branch
          cloningStatus {
            message
            status
          }
          credentials {
            id
            isToken
            name
            type
          }
          environment
          gitEnvironmentUrls {
            url
            id
            createdAt
            createdBy
            urlType
          }
          gitignore
          id
          includesHealthCheck
          nickname
          state
          url
          useVpn
          createdAt
          createdBy
          lastEditedAt
          lastEditedBy
        }
        ... on IPRoot {
          address
          id
          nickname
          state
        }
        ... on URLRoot {
          host
          id
          nickname
          path
          port
          protocol
          query
          state
        }
      }
    }
  }
`;

const GET_ROOT: DocumentNode = gql`
  query GetRoot($groupName: String!, $rootId: ID!) {
    root(groupName: $groupName, rootId: $rootId) {
      ... on GitRoot {
        id
        secrets {
          description
          key
          value
        }
        gitEnvironmentUrls {
          url
          id
          secrets {
            value
            key
            description
          }
          urlType
        }
      }
      ... on URLRoot {
        id
        secrets {
          description
          key
          value
        }
      }
    }
  }
`;
const GET_ROOT_ENVIRONMENT_URLS: DocumentNode = gql`
  query GetRootEnvironmentUrls($groupName: String!, $rootId: ID!) {
    root(groupName: $groupName, rootId: $rootId) {
      ... on GitRoot {
        id
        gitEnvironmentUrls {
          url
          id
          urlType
        }
      }
    }
  }
`;

const GET_GIT_ROOT_DETAILS = gql`
  query GetGitRootDetails($groupName: String!, $rootId: ID!) {
    root(groupName: $groupName, rootId: $rootId) {
      ... on GitRoot {
        cloningStatus {
          message
          status
        }
        environment
        gitignore
        id
        lastCloningStatusUpdate
        lastStateStatusUpdate
        nickname
        useVpn
      }
    }
  }
`;

const GET_ORGANIZATION_CREDENTIALS: DocumentNode = gql`
  query GetOrganizationCredentials($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      name
      credentials {
        __typename
        id
        isPat
        isToken
        name
        owner
        type
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

const ADD_SECRET: DocumentNode = gql`
  mutation AddSecret(
    $rootId: ID!
    $key: String!
    $value: String!
    $groupName: String!
    $description: String
  ) {
    addSecret(
      rootId: $rootId
      key: $key
      value: $value
      groupName: $groupName
      description: $description
    ) {
      success
    }
  }
`;
const ADD_ENVIRONMENT_SECRET: DocumentNode = gql`
  mutation AddSecret(
    $urlId: String!
    $key: String!
    $value: String!
    $groupName: String!
    $description: String
  ) {
    addGitEnvironmentSecret(
      urlId: $urlId
      key: $key
      value: $value
      description: $description
      groupName: $groupName
    ) {
      success
    }
  }
`;
const ADD_ENVIRONMENT_URL: DocumentNode = gql`
  mutation AddGitEnvironmentUrl(
    $cloudName: String
    $groupName: String!
    $rootId: ID!
    $url: String!
    $urlType: GitEnvironmentCloud!
  ) {
    addGitEnvironmentUrl(
      groupName: $groupName
      rootId: $rootId
      url: $url
      urlType: $urlType
      cloudName: $cloudName
    ) {
      urlId
      success
    }
  }
`;
const REMOVE_SECRET: DocumentNode = gql`
  mutation RemoveSecret($groupName: String!, $rootId: ID!, $key: String!) {
    removeSecret(rootId: $rootId, key: $key, groupName: $groupName) {
      success
    }
  }
`;
const REMOVE_ENVIRONMENT_URL_SECRET: DocumentNode = gql`
  mutation RemoveEnvironmentUrlSecret(
    $urlId: String!
    $key: String!
    $groupName: String!
  ) {
    removeEnvironmentUrlSecret(
      urlId: $urlId
      key: $key
      groupName: $groupName
    ) {
      success
    }
  }
`;

const UPDATE_GIT_ROOT: DocumentNode = gql`
  mutation UpdateGitRoot(
    $branch: String!
    $credentials: RootCredentialsInput
    $environment: String!
    $gitignore: [String!]!
    $groupName: String!
    $id: ID!
    $includesHealthCheck: Boolean!
    $nickname: String
    $url: String!
    $useVpn: Boolean!
  ) {
    updateGitRoot(
      branch: $branch
      credentials: $credentials
      environment: $environment
      gitignore: $gitignore
      groupName: $groupName
      id: $id
      nickname: $nickname
      includesHealthCheck: $includesHealthCheck
      url: $url
      useVpn: $useVpn
    ) {
      success
    }
  }
`;

const UPDATE_IP_ROOT: DocumentNode = gql`
  mutation UpdateIpRoot($groupName: String!, $rootId: ID!, $nickname: String!) {
    updateIpRoot(groupName: $groupName, rootId: $rootId, nickname: $nickname) {
      success
    }
  }
`;

const UPDATE_URL_ROOT: DocumentNode = gql`
  mutation UpdateUrlRoot(
    $groupName: String!
    $rootId: ID!
    $nickname: String!
  ) {
    updateUrlRoot(groupName: $groupName, rootId: $rootId, nickname: $nickname) {
      success
    }
  }
`;

const ADD_IP_ROOT = gql`
  mutation AddIpRoot(
    $address: String!
    $groupName: String!
    $nickname: String!
  ) {
    addIpRoot(address: $address, groupName: $groupName, nickname: $nickname) {
      success
    }
  }
`;

const ADD_URL_ROOT = gql`
  mutation AddUrlRoot($url: String!, $groupName: String!, $nickname: String!) {
    addUrlRoot(url: $url, groupName: $groupName, nickname: $nickname) {
      success
    }
  }
`;

const ACTIVATE_ROOT: DocumentNode = gql`
  mutation ActivateRoot($groupName: String!, $id: ID!) {
    activateRoot(groupName: $groupName, id: $id) {
      success
    }
  }
`;

const DEACTIVATE_ROOT: DocumentNode = gql`
  mutation DeactivateRoot(
    $groupName: String!
    $id: ID!
    $other: String
    $reason: RootDeactivationReason!
  ) {
    deactivateRoot(
      groupName: $groupName
      id: $id
      other: $other
      reason: $reason
    ) {
      success
    }
  }
`;

const MOVE_ROOT: DocumentNode = gql`
  mutation MoveRoot($groupName: String!, $id: ID!, $targetGroupName: String!) {
    moveRoot(
      groupName: $groupName
      id: $id
      targetGroupName: $targetGroupName
    ) {
      success
    }
  }
`;

const GET_GROUPS: DocumentNode = gql`
  query GetGroups {
    me {
      organizations {
        groups {
          name
          organization
          service
        }
        name
      }
      userEmail
    }
  }
`;
const GET_ENVIRONMENT_URL: DocumentNode = gql`
  query GetEnvironmentUrl($groupName: String!, $urlId: String!) {
    environmentUrl(groupName: $groupName, urlId: $urlId) {
      id
      url
      createdAt
      secrets {
        key
        value
        description
      }
    }
  }
`;

const GET_ROOTS_VULNS: DocumentNode = gql`
  query GetRootsVulns($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          id
          vulnerabilities {
            id
            vulnerabilityType
          }
        }
        ... on IPRoot {
          id
          vulnerabilities {
            id
            vulnerabilityType
          }
        }
        ... on URLRoot {
          id
          vulnerabilities {
            id
            vulnerabilityType
          }
        }
      }
    }
  }
`;

const VERIFY_AWS_CREDENTIALS: DocumentNode = gql`
  query VerifyAwsCredentials($accessKeyId: String!, $secretAccessKey: String!) {
    verifyAwsCredentials(
      accessKeyId: $accessKeyId
      secretAccessKey: $secretAccessKey
    )
  }
`;

const VERIFY_URL_STATUS: DocumentNode = gql`
  query verifyUrlStatus($url: String!) {
    verifyUrlStatus(url: $url)
  }
`;

const SYNC_GIT_ROOT: DocumentNode = gql`
  mutation SyncGitRoot($groupName: String!, $rootId: String!) {
    syncGitRoot(groupName: $groupName, rootId: $rootId) {
      success
    }
  }
`;

const VALIDATE_GIT_ACCESS: DocumentNode = gql`
  mutation ValidateGitAccess(
    $branch: String!
    $credentials: RootCredentialsInput!
    $url: String!
  ) {
    validateGitAccess(branch: $branch, credentials: $credentials, url: $url) {
      success
    }
  }
`;

const REMOVE_ENVIRONMENT_URL: DocumentNode = gql`
  mutation RemoveEnvironmentUrl(
    $urlId: String!
    $rootId: ID!
    $groupName: String!
  ) {
    removeEnvironmentUrl(
      urlId: $urlId
      rootId: $rootId
      groupName: $groupName
    ) {
      success
    }
  }
`;

export {
  ACTIVATE_ROOT,
  ADD_ENVIRONMENT_SECRET,
  ADD_ENVIRONMENT_URL,
  ADD_GIT_ROOT,
  ADD_IP_ROOT,
  ADD_SECRET,
  ADD_URL_ROOT,
  DEACTIVATE_ROOT,
  GET_GIT_ROOT_DETAILS,
  GET_GROUPS,
  GET_ROOTS_VULNS,
  GET_ENVIRONMENT_URL,
  GET_ROOT,
  GET_ROOTS,
  GET_ORGANIZATION_CREDENTIALS,
  MOVE_ROOT,
  REMOVE_SECRET,
  SYNC_GIT_ROOT,
  UPDATE_GIT_ROOT,
  UPDATE_IP_ROOT,
  UPDATE_URL_ROOT,
  VALIDATE_GIT_ACCESS,
  REMOVE_ENVIRONMENT_URL,
  REMOVE_ENVIRONMENT_URL_SECRET,
  GET_ROOT_ENVIRONMENT_URLS,
  VERIFY_AWS_CREDENTIALS,
  VERIFY_URL_STATUS,
};
