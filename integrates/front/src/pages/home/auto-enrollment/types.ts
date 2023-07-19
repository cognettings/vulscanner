interface IAutoenrollment {
  initialPage?: TEnrollPages;
  trialGroupName?: string;
  trialOrgName?: string;
  trialOrgId?: string;
}
interface IAddGitRootResult {
  addGitRoot: {
    success: boolean;
  };
}

interface IAddGroupResult {
  addGroup: {
    success: boolean;
  };
}

interface IAddOrganizationResult {
  addOrganization: {
    organization: {
      id: string;
      name: string;
    };
    success: boolean;
  };
}

interface IAddRootProps {
  initialValues: IRootAttr;
  mutationsState: {
    group: boolean;
    organization: boolean;
  };
  organizationValues: IOrgAttr;
  rootMessages: {
    message: string;
    type: string;
  };
  setPage: React.Dispatch<React.SetStateAction<TEnrollPages>>;
  setProgress: React.Dispatch<React.SetStateAction<number>>;
  setRepositoryValues: React.Dispatch<React.SetStateAction<IRootAttr>>;
  setRootMessages: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >;
}

type IAlertMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

interface ICheckGitAccessResult {
  validateGitAccess: {
    success: boolean;
  };
}

interface IGetStakeholderGroupsResult {
  me: {
    organizations: {
      country: string;
      groups: {
        name: string;
      }[];
      name: string;
    }[];
    trial: {
      completed: boolean;
      startDate: string;
    } | null;
    userEmail: string;
    userName: string;
  };
}

interface IRootAttr {
  branch: string;
  credentials: {
    auth: "TOKEN" | "USER";
    azureOrganization: string | undefined;
    isPat: boolean;
    key: string;
    name: string;
    password: string;
    token: string;
    type: "" | "HTTPS" | "SSH";
    typeCredential: "" | "OAUTH" | "SSH" | "TOKEN" | "USER";
    user: string;
  };
  env: string;
  exclusions: string[];
  hasExclusions: string;
  url: string;
}

interface IOrgAttr {
  groupDescription: string;
  groupName: string;
  organizationCountry: string;
  organizationName: string;
  reportLanguage: string;
  terms: string[];
}

type TEnrollPages = "fastTrack" | "oauthRepoForm" | "repository" | "standBy";

export type {
  IAddGitRootResult,
  IAddGroupResult,
  IAddOrganizationResult,
  IAddRootProps,
  IAlertMessages,
  IAutoenrollment,
  ICheckGitAccessResult,
  IGetStakeholderGroupsResult,
  IOrgAttr,
  IRootAttr,
  TEnrollPages,
};
