import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

interface IGroup {
  name: string;
  permissions: string[];
  serviceAttributes: string[];
}

interface IOrganization {
  groups: IGroup[];
  name: string;
}

interface IUserOrganizationsGroups {
  me: {
    organizations: IOrganization[];
    userEmail: string;
  };
}

const GET_USER_ORGANIZATIONS_GROUPS = gql`
  query GetUserOrganizationsGroups {
    me {
      organizations {
        groups {
          name
          permissions
          serviceAttributes
        }
        name
      }
      userEmail
    }
  }
`;

const REQUEST_GROUPS_UPGRADE_MUTATION: DocumentNode = gql`
  mutation RequestGroupsUpgrade($groupNames: [String!]!) {
    requestGroupsUpgrade(groupNames: $groupNames) {
      success
    }
  }
`;

export type { IUserOrganizationsGroups, IGroup };
export { GET_USER_ORGANIZATIONS_GROUPS, REQUEST_GROUPS_UPGRADE_MUTATION };
