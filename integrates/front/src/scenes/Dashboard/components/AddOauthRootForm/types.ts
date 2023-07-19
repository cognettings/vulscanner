declare type CloningStatusType = "FAIL" | "N/A" | "OK" | "QUEUED" | "UNKNOWN";
declare type Provider = "" | "AZURE" | "BITBUCKET" | "GITHUB" | "GITLAB";

interface IOauthRootFormProps {
  closeModal?: () => void;
  initialValues?: IFormValues;
  onUpdate?: () => void;
  trialGroupName?: string;
  trialOrgId?: string;
  provider?: Provider;
  setIsCredentialSelected?: React.Dispatch<React.SetStateAction<boolean>>;
  setProgress?: React.Dispatch<React.SetStateAction<number>>;
}

interface ISecret {
  description: string;
  key: string;
  value: string;
}

interface IEnvironmentUrl {
  cloudName: string | undefined;
  id: string;
  url: string;
  secrets: ISecret[];
  createdAt: Date | null;
  createdBy: string | null;
  urlType: string;
}

interface ICredentialsAttr {
  id: string;
  isPat: boolean;
  isToken: boolean;
  name: string;
  oauthType: "" | "AZURE" | "BITBUCKET" | "GITHUB" | "GITLAB";
  type: "" | "HTTPS" | "OAUTH" | "SSH" | "TOKEN";
}

interface IGitignore {
  paths: string[];
}

interface IFormValues {
  allChecked: boolean;
  branches: string[];
  cloningStatus: {
    message: string;
    status: CloningStatusType;
  };
  credentials: ICredentialsAttr;
  environments: string[];
  environmentUrls: string[];
  gitEnvironmentUrls: IEnvironmentUrl[];
  gitignore: IGitignore[];
  hasExclusions: string;
  healthCheckConfirm: string[] | undefined;
  id: string;
  includesHealthCheck: string;
  reposByName: string;
  secrets: ISecret[];
  state: "ACTIVE" | "INACTIVE";
  urls: string[];
}

interface IIntegrationRepository {
  branches: string[];
  name: string;
  url: string;
}

export type {
  ICredentialsAttr,
  IEnvironmentUrl,
  IFormValues,
  IGitignore,
  IIntegrationRepository,
  IOauthRootFormProps,
  ISecret,
  Provider,
};
