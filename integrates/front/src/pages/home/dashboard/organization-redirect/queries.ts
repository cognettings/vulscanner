import { gql } from "@apollo/client";

interface IGroupOrganization {
  group: {
    name: string;
    organization: string;
  };
}

const GET_GROUP_ORGANIZATION = gql`
  query GetGroupOrganization($groupName: String!) {
    group(groupName: $groupName) {
      name
      organization
    }
  }
`;

interface IPortfolioOrganization {
  tag: {
    name: string;
    organization: string;
  };
}

const GET_PORTFOLIO_ORGANIZATION = gql`
  query GetPortfolioOrganization($tagName: String!) {
    tag(tag: $tagName) {
      name
      organization
    }
  }
`;

export { GET_GROUP_ORGANIZATION, GET_PORTFOLIO_ORGANIZATION };
export type { IGroupOrganization, IPortfolioOrganization };
