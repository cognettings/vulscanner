interface IOrganizationPermission {
  organization: {
    permissions: string[];
  };
}

interface IGetOrganizationId {
  organizationId: {
    __typename: "Organization";
    id: string;
    name: string;
  };
}

interface IGetUserPortfolios {
  me: {
    tags: {
      name: string;
      groups: {
        name: string;
      }[];
    }[];
    userEmail: string;
  };
}

export type { IGetOrganizationId, IGetUserPortfolios, IOrganizationPermission };
