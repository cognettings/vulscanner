import type { Provider } from "../../types";

interface IAddRootProps {
  manualClick: () => void;
  providersClick: (provider: Provider) => void;
}

interface ICredentialsAttr {
  azureOrganization: string | null;
  id: string;
  isPat: boolean;
  isToken: boolean;
  name: string;
  oauthType: "" | "AZURE" | "BITBUCKET" | "GITHUB" | "GITLAB";
  owner: string;
  type: "HTTPS" | "OAUTH" | "SSH";
}

export type { IAddRootProps, ICredentialsAttr };
