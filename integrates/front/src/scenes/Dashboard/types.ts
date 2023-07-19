import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IAddStakeholderAttr {
  addStakeholder: {
    email: string;
    success: boolean;
  };
}

interface IUser {
  me: {
    __typename: "Me";
    isConcurrentSession: boolean;
    role: string;
    remember: boolean;
    sessionExpiration: string;
    userEmail: string;
    userName: string;
  };
}

interface IOrganizationGroups {
  groups: IGroups[];
  name: string;
}

interface IGroups {
  name: string;
  permissions: string[];
  serviceAttributes: string[];
}

interface IGetUserOrganizationsGroups {
  me: {
    organizations: IOrganizationGroups[];
    userEmail: string;
  };
}

interface IGetMeVulnerabilitiesAssigned {
  me: {
    vulnerabilitiesAssigned: IVulnRowAttr[];
    userEmail: string;
  };
}

export type {
  IAddStakeholderAttr,
  IGetMeVulnerabilitiesAssigned,
  IGetUserOrganizationsGroups,
  IGroups,
  IOrganizationGroups,
  IUser,
};
