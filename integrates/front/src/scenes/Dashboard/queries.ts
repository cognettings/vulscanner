import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ACCEPT_LEGAL_MUTATION: DocumentNode = gql`
  mutation AcceptLegalMutation($remember: Boolean!) {
    acceptLegal(remember: $remember) {
      success
    }
  }
`;

const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation AddStakeholderMutation($email: String!, $role: StakeholderRole!) {
    addStakeholder(email: $email, role: $role) {
      success
      email
    }
  }
`;

const GET_ORG_LEVEL_PERMISSIONS: DocumentNode = gql`
  query GetOrgLevelPermissions($identifier: String!) {
    organization(organizationId: $identifier) {
      name
      permissions
    }
  }
`;

const GET_GROUP_LEVEL_PERMISSIONS: DocumentNode = gql`
  query GetGroupLevelPermissions($identifier: String!) {
    group(groupName: $identifier) {
      name
      permissions
    }
  }
`;

const GET_USER: DocumentNode = gql`
  query GetUser {
    me(callerOrigin: "FRONT") {
      isConcurrentSession
      remember
      role
      sessionExpiration
      userEmail
      userName
    }
  }
`;

const GET_USER_ORGANIZATIONS_GROUPS: DocumentNode = gql`
  query GetUserOrganizationsGroups {
    me(callerOrigin: "FRONT") {
      organizations {
        groups {
          name
          permissions
          serviceAttributes
        }
        name
      }
      userEmail
      __typename
    }
  }
`;

export {
  ACCEPT_LEGAL_MUTATION,
  ADD_STAKEHOLDER_MUTATION,
  GET_USER,
  GET_ORG_LEVEL_PERMISSIONS,
  GET_GROUP_LEVEL_PERMISSIONS,
  GET_USER_ORGANIZATIONS_GROUPS,
};
