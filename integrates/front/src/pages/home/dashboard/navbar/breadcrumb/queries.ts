import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_TITLE: DocumentNode = gql`
  query GetFindingTitle($findingId: String!) {
    finding(identifier: $findingId) {
      id
      title
    }
  }
`;

const GET_ORGANIZATION_GROUP_NAMES: DocumentNode = gql`
  query GetOrganizationGroupNames($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      groups {
        name
      }
    }
  }
`;

interface IUserOrganizations {
  me: {
    __typename: "Me";
    organizations: {
      __typename: "Organization";
      name: string;
    }[];
    userEmail: string;
  };
}

const GET_USER_ORGANIZATIONS: DocumentNode = gql`
  query GetUserOrganizations {
    me(callerOrigin: "FRONT") {
      organizations {
        name
      }
      userEmail
      __typename
    }
  }
`;

const GET_USER_TAGS: DocumentNode = gql`
  query GetUserTags($organizationId: String!) {
    me(callerOrigin: "FRONT") {
      tags(organizationId: $organizationId) {
        name
      }
      userEmail
      __typename
    }
  }
`;

export type { IUserOrganizations };
export {
  GET_FINDING_TITLE,
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
};
