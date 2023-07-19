import { gql } from "@apollo/client";

interface IBilling {
  authors: { actor: string }[];
}

interface IGroupBilling {
  group: {
    billing: IBilling;
    name: string;
  };
}

const GET_GROUP_BILLING = gql`
  query GetGroupBilling($groupName: String!) {
    group(groupName: $groupName) {
      billing {
        authors {
          actor
        }
      }
      name
    }
  }
`;

interface IOrganizationBilling {
  organization: {
    billing: IBilling;
    name: string;
  };
}

const GET_ORGANIZATION_BILLING = gql`
  query GetOrganizationBilling($organizationId: String!) {
    organization(organizationId: $organizationId) {
      billing {
        authors {
          actor
        }
      }
      name
    }
  }
`;

export { GET_GROUP_BILLING, GET_ORGANIZATION_BILLING };
export type { IGroupBilling, IOrganizationBilling };
